from django.contrib import admin

from .models import Machine, Metric, Incident


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "endpoint")


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = (
        "id", "machine", "cpu", "mem", "disk", "uptime", "requested_at"
    )
    list_filter = ("machine",)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "machine", "overload_type", "detected_at", "is_active"
    )
    list_filter = ("machine", "overload_type")
