import random

from aiohttp import web

from monitor.constants import (
    CPU_MIN_VALUE_IN_PERCENTS,
    MEM_MIN_VALUE_IN_PERCENTS,
    DISK_MIN_VALUE_IN_PERCENTS,
    MAX_VALUE_IN_PERCENTS,
    MIN_VALUE,
    SECS_IN_MINUTE,
    MINS_IN_HOUR,
    HOURS_IN_DAY,
    HOST,
    PORT,
    COUNT_MACHINES,
)


async def handler(request):
    cpu = random.randint(CPU_MIN_VALUE_IN_PERCENTS, MAX_VALUE_IN_PERCENTS)
    mem = random.randint(MEM_MIN_VALUE_IN_PERCENTS, MAX_VALUE_IN_PERCENTS)
    disk = random.randint(DISK_MIN_VALUE_IN_PERCENTS, MAX_VALUE_IN_PERCENTS)
    uptime = (
        f"{random.randint(MIN_VALUE, 10)}d "
        f"{random.randint(MIN_VALUE, HOURS_IN_DAY)}h "
        f"{random.randint(MIN_VALUE, MINS_IN_HOUR)}m "
        f"{random.randint(MIN_VALUE, SECS_IN_MINUTE)}s"
    )
    return web.json_response(
        {
            "cpu": cpu,
            "mem": mem,
            "disk": disk,
            "uptime": uptime,
        }
    )


app = web.Application()

for i in range(1, COUNT_MACHINES + 1):
    app.router.add_get(f"/machine/{i}", handler, allow_head=True)
app.router.add_get("/machine/{id}", handler, allow_head=True)

if __name__ == "__main__":
    web.run_app(app, host=HOST, port=PORT)
