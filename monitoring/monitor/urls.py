from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="monitor_index"),
    path("machine/<int:id>/", views.machine_view, name="machine"),
]
