from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    ROLES = (
        ('paciente', 'Paciente'),
        ('doctor', 'Doctor'),
        ('rrhh', 'RRHH'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='paciente')

    def es_paciente(self):
        return self.rol == 'paciente'
    def es_doctor(self):
        return self.rol == 'doctor'
    def es_rrhh(self):
        return self.rol == 'rrhh'


class Doctor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_doctor')
    especialidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name() or self.usuario.username}"


class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_paciente')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Horario(models.Model):
    DIAS = [
        (0,'Lunes'),(1,'Martes'),(2,'Miércoles'),(3,'Jueves'),
        (4,'Viernes'),(5,'Sábado'),(6,'Domingo')
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['doctor', 'dia_semana', 'hora_inicio']
        unique_together = ('doctor','dia_semana','hora_inicio','hora_fin')

    def __str__(self):
        return f"{self.doctor} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class Cita(models.Model):
    ESTADOS = (
        ('pendiente','Pendiente'),
        ('atendida','Atendida'),
        ('cancelada','Cancelada'),
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    motivo = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Cita con {self.doctor} - {self.fecha_hora}"


class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historial')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField()
    creada_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-creada_en']

    def __str__(self):
        return f"Historial {self.paciente} - {self.creada_en:%Y-%m-%d}"
