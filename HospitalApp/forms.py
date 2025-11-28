from django import forms
from .models import Cita, Horario

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'fecha_hora', 'motivo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['doctor','dia_semana','hora_inicio','hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type':'time'}),
            'hora_fin': forms.TimeInput(attrs={'type':'time'})
        }
