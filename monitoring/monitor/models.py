from django.db import models

from .constants import (
    SMALL_CHAR_LEN_FIELD,
    CHOICES_LEN_FIELD,
    DATETIME_FORMAT,
    CPU_CODE_NAME,
    MEM_CODE_NAME,
    DISK_CODE_NAME,
)


class Machine(models.Model):
    name = models.CharField(max_length=SMALL_CHAR_LEN_FIELD)
    endpoint = models.URLField(help_text="Полный URL к HTTP-эндпоинту")

    def __str__(self):
        return f"{self.name} ({self.endpoint})"


class Metric(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="metrics",
    )
    cpu = models.SmallIntegerField()
    mem = models.SmallIntegerField()
    disk = models.SmallIntegerField()
    uptime = models.CharField(max_length=SMALL_CHAR_LEN_FIELD)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-requested_at",)

    def __str__(self):
        return (
            f"Статистика по {self.machine.name} "
            f"в {self.requested_at.strftime(DATETIME_FORMAT)}"
        )


class Incident(models.Model):
    TYPE_CHOICES = [
        (CPU_CODE_NAME, "CPU"),
        (MEM_CODE_NAME, "Memory"),
        (DISK_CODE_NAME, "Disk"),
    ]
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="incidents",
    )
    overload_type = models.CharField(
        max_length=CHOICES_LEN_FIELD,
        choices=TYPE_CHOICES,
    )
    detected_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-detected_at",)

    def __str__(self):
        return (
            f"[{self.overload_type.upper()}] {self.machine.name} "
            f"({'active' if self.active else 'closed'})"
        )
