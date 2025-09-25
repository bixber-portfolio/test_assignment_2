from http import HTTPStatus

from django.shortcuts import render
from django.http import JsonResponse

from .models import Machine


def index(request):
    machines = Machine.objects.all().prefetch_related("metrics")
    data = []
    for machine in machines:
        latest = machine.metrics.first()
        data.append({"machine": machine, "metric": latest})
    return render(request, "monitor/index.html", {"data": data})


def machine_view(request, id):
    try:
        machine = Machine.objects.get(id=id)
    except Machine.DoesNotExist:
        return JsonResponse(
            {"error": f"Machine {id} not found"},
            status=HTTPStatus.NOT_FOUND,
        )

    metric = machine.metrics.order_by("-requested_at").first()
    if not metric:
        return JsonResponse(
            {"error": "No metrics for this machine"},
            status=HTTPStatus.NOT_FOUND,
        )

    data = {
        "cpu": f"{metric.cpu}%",
        "mem": f"{metric.mem}%",
        "disk": f"{metric.disk}%",
        "uptime": metric.uptime,
    }
    return JsonResponse(data)
