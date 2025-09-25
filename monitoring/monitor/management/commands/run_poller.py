import asyncio
from datetime import datetime as dt
from http import HTTPStatus

import aiohttp
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from monitor.models import Machine, Metric
from monitor.services import check_metric
from monitor.constants import (
    TIMEOUT_IN_SECONDS,
    DEFAULT_INTERVAL_IN_SECONDS,
    DEFAULT_CONCURRENSY_LIMIT,
    SECS_IN_MINUTE,
    DATETIME_FORMAT,
)


async def fetch(session, machine):
    try:
        async with session.get(
            machine.endpoint,
            timeout=TIMEOUT_IN_SECONDS,
        ) as resp:
            if resp.status == HTTPStatus.OK:
                data = await resp.json()
                metric = await sync_to_async(Metric.objects.create)(
                    machine=machine,
                    cpu=int(data.get("cpu", "")),
                    mem=int(data.get("mem", "")),
                    disk=int(data.get("disk", "")),
                    uptime=str(data.get("uptime", "")),
                )
                await sync_to_async(check_metric)(metric)
                print(f"[+] {machine} OK")
            else:
                print(f"[{resp.status}] {machine}")
    except Exception as e:
        print(f"[!] Ошибка чтения {machine.endpoint}: {e}")


async def poll_once(concurrency=DEFAULT_CONCURRENSY_LIMIT):
    if not await sync_to_async(Machine.objects.exists)():
        print("Нет зарегистрированных машин для опроса")
        return
    else:
        machines = list(await sync_to_async(list)(Machine.objects.all()))
        sem = asyncio.Semaphore(concurrency)
        async with aiohttp.ClientSession() as session:
            async def sem_fetch(m):
                async with sem:
                    await fetch(session, m)
            await asyncio.gather(*(sem_fetch(m) for m in machines))


class Command(BaseCommand):
    help = (
        "Запустить поллинг: "
        "периодически опрашивать эндпоинты машины и сохранять результаты"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=DEFAULT_INTERVAL_IN_SECONDS,
        )
        parser.add_argument(
            "--concurrency",
            type=int,
            default=DEFAULT_CONCURRENSY_LIMIT,
        )

    def handle(self, *args, **options):
        interval = options["interval"]
        concurrency = options["concurrency"]
        if Machine.objects.exists():
            print(
                f"Опрос начался c параметрами:\n"
                f"Интервал: {interval // SECS_IN_MINUTE} минут\n"
                f"Количество одновременных запросов: {concurrency}"
            )
            loop = asyncio.get_event_loop()
            try:
                while True:
                    print(
                        "Цикл опроса начался в",
                        dt.now().strftime(DATETIME_FORMAT),
                    )
                    loop.run_until_complete(poll_once(concurrency=concurrency))
                    print("Цикл опроса завершен. Ожидание...")
                    loop.run_until_complete(asyncio.sleep(interval))
            except KeyboardInterrupt:
                print("Цикл опроса остановлен пользователем")
        else:
            print(
                "Машин в системе нет. Зарегистрируйте хотя бы одну машину "
                "и попробуйте запустить программу заново"
            )
