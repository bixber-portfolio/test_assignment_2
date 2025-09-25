from datetime import timedelta

from django.db.models import Max
from asgiref.sync import sync_to_async

from .constants import (
    CPU_LIMIT_IN_PERCENTS,
    MEM_LIMIT_IN_PERCENTS,
    DISK_LIMIT_IN_PERCENTS,
    MEM_LIMIT_TIME_IN_MINS,
    DISK_LIMIT_TIME_IN_HOURS,
    CPU_CODE_NAME,
    MEM_CODE_NAME,
    DISK_CODE_NAME,
    DEFAULT_INTERVAL_IN_MINUTES,
    MINS_IN_HOUR,
)
from .models import Metric, Incident


async def get_object_from_metrics(id):
    return await sync_to_async(Metric.objects.get)(id=id)


def get_recent_metrics(hours=0, minutes=0):
    """
    Возвращает все метрики за определенный промежуток времени.
    """
    last_time = Metric.objects.aggregate(last=Max('requested_at'))['last']
    if not last_time:
        return Metric.objects.none()

    interval_start = last_time - timedelta(hours=hours, minutes=minutes)
    return Metric.objects.filter(
        requested_at__gte=interval_start,
        requested_at__lte=last_time
    ).order_by('requested_at')


def check_metric(metric: Metric):
    """
    Проверить метрики и зафиксировать инциденты
    """
    if metric.cpu is not None and metric.cpu > CPU_LIMIT_IN_PERCENTS:
        if not Incident.objects.filter(
            machine=metric.machine,
            overload_type=CPU_CODE_NAME,
            is_active=True,
        ).exists():
            create_incident(metric.machine, CPU_CODE_NAME)

    if metric.mem is not None:
        recent_metrics = get_recent_metrics(minutes=MEM_LIMIT_TIME_IN_MINS)
        machine_metrics = recent_metrics.filter(machine=metric.machine)
        mem_values = list(machine_metrics.values_list(
            MEM_CODE_NAME,
            flat=True,
        ))
        if (
            mem_values
            and len(mem_values) > (
                MEM_LIMIT_TIME_IN_MINS // DEFAULT_INTERVAL_IN_MINUTES
            )
            and all(m > MEM_LIMIT_IN_PERCENTS for m in mem_values)
            and not Incident.objects.filter(
                machine=metric.machine,
                overload_type=MEM_CODE_NAME,
                is_active=True,
            ).exists()
        ):
            create_incident(metric.machine, MEM_CODE_NAME)

    if metric.disk is not None:
        recent_metrics = get_recent_metrics(minutes=DISK_LIMIT_TIME_IN_HOURS)
        machine_metrics = recent_metrics.filter(machine=metric.machine)
        disk_values = list(machine_metrics.values_list(
            DISK_CODE_NAME,
            flat=True
        ))
        if (
            disk_values
            and len(disk_values) > (
                (DISK_LIMIT_TIME_IN_HOURS * MINS_IN_HOUR)
                // DEFAULT_INTERVAL_IN_MINUTES
            )
            and all(m > DISK_LIMIT_IN_PERCENTS for m in disk_values)
            and not Incident.objects.filter(
                machine=metric.machine,
                overload_type=DISK_CODE_NAME,
                is_active=True,
            ).exists()
        ):
            create_incident(metric.machine, MEM_CODE_NAME)


def create_incident(machine, type):
    """
    Создать новый инцидент, если нет такого же активного
    """
    active_exists = Incident.objects.filter(
        machine=machine,
        overload_type=type,
        is_active=True,
    ).exists()
    if not active_exists:
        Incident.objects.create(machine=machine, overload_type=type)
