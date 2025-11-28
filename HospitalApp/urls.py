from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),

    # Redirección por rol
    path("redirigir/", views.redirigir_por_rol, name="redirigir"),

    # PACIENTE
    path("paciente/citas/nueva/", views.paciente_crear_cita, name="paciente_crear_cita"),
    path("paciente/citas/", views.paciente_mis_citas, name="paciente_mis_citas"),

    # DOCTOR
    path("doctor/citas/", views.doctor_citas, name="doctor_citas"),
    path("doctor/citas/<int:cita_id>/atender/", views.doctor_marcar_atendida, name="doctor_marcar_atendida"),
    path("doctor/historial/<int:paciente_id>/", views.doctor_historial_paciente, name="doctor_historial_paciente"),

    # RRHH
    path("rrhh/horarios/", views.rrhh_horarios, name="rrhh_horarios"),
    path("rrhh/horarios/nuevo/", views.rrhh_crear_horario, name="rrhh_crear_horario"),
]
