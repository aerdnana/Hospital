from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Cita, Doctor, Paciente, HistorialMedico, Horario
from .forms import CitaForm, HorarioForm
from django.shortcuts import redirect
from datetime import datetime


def inicio(request):
    return render(request, "hospital/index.html")

@login_required
def redirigir_por_rol(request):
    usuario = request.user

    if usuario.rol == "paciente":
        return redirect("paciente_crear_cita")

    elif usuario.rol == "doctor":
        return redirect("doctor_citas")

    elif usuario.rol == "rrhh":
        return redirect("rrhh_horarios")

    return redirect("inicio")

# ---------- PACIENTE ----------
@login_required
def paciente_crear_cita(request):

    if request.user.rol != "paciente":
        return redirect("redirigir")

    paciente = request.user.perfil_paciente

    if request.method == "POST":
        doctor_id = request.POST["doctor_id"]
        fecha_hora_str = request.POST["fecha"]  # formato: 2025-11-29T08:20

        fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%dT%H:%M")

        doctor = Doctor.objects.get(id=doctor_id)

        Cita.objects.create(
            paciente=paciente,
            doctor=doctor,
            fecha_hora=fecha_hora
        )

        return redirect("paciente_mis_citas")

    doctores = Doctor.objects.all()
    return render(request, "hospital/crear_cita.html", {"doctores": doctores})




@login_required
def paciente_mis_citas(request):
    if not request.user.es_paciente():
        return HttpResponseForbidden("No tienes permiso.")
    paciente = request.user.perfil_paciente
    citas = paciente.citas.all()
    return render(request, "hospital/paciente_mis_citas.html", {"citas": citas})

# ---------- DOCTOR ----------
@login_required
def doctor_citas(request):
    if request.user.rol != "doctor":
        return redirect("redirigir")


    if not request.user.es_doctor():
        return HttpResponseForbidden("No tienes permiso.")
    doctor = request.user.perfil_doctor
    citas = doctor.citas.all()
    return render(request, "hospital/doctor_citas.html", {"citas":citas})


@login_required
def doctor_marcar_atendida(request, cita_id):
    doctor = request.user.perfil_doctor
    cita = Cita.objects.get(id=cita_id, doctor=doctor)

    cita.estado = "atendida"
    cita.save()

    return redirect("doctor_citas")


@login_required
def doctor_historial_paciente(request, paciente_id):
    if not request.user.es_doctor():
        return HttpResponseForbidden("No tienes permiso.")

    paciente = get_object_or_404(Paciente, id=paciente_id)
    historial = paciente.historial.all()
    return render(request, "hospital/doctor_historial_paciente.html", {
        "paciente": paciente,
        "historial": historial
    })


# ---------- RRHH ----------
@login_required
def rrhh_horarios(request):
    if request.user.rol != "rrhh":
        return redirect("redirigir")
        
    if not request.user.es_rrhh():
        return HttpResponseForbidden("No tienes permiso.")

    horarios = Horario.objects.all()
    return render(request, "hospital/rrhh_horarios_lista.html", {"horarios":horarios})


@login_required
def rrhh_crear_horario(request):
    if not request.user.es_rrhh():
        return HttpResponseForbidden("No tienes permiso.")

    if request.method == "POST":
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hospital:rrhh_horarios")
    else:
        form = HorarioForm()

    return render(request, "hospital/rrhh_horarios_form.html", {"form":form})
