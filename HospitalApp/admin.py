from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Doctor, Paciente, Horario, Cita, HistorialMedico

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Rol", {"fields": ("rol",)}),
    )

admin.site.register(Doctor)
admin.site.register(Paciente)
admin.site.register(Horario)
admin.site.register(Cita)
admin.site.register(HistorialMedico)
