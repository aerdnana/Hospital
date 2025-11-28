# Sistema de Gestión Hospitalaria

Aplicación desarrollada en Django que permite gestionar citas médicas y controlar el acceso según el rol del usuario: Paciente, Doctor y RRHH.  
Cada usuario es redirigido automáticamente a su panel correspondiente tras iniciar sesión.
Para el curso de Ing Software 2

---

## Instalación

```bash
    python -m venv venv
    venv\Scripts\activate   # En Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

 Crear usuarios de prueba

Ejecuta:
```bash
    python manage.py shell
```

y

from HospitalApp.models import Usuario, Paciente, Doctor

# Paciente
u = Usuario.objects.create_user("paciente1", password="123", rol="paciente")
Paciente.objects.create(usuario=u)

# Doctor
d = Usuario.objects.create_user("doctor1", password="123", rol="doctor")
Doctor.objects.create(usuario=d)

# RRHH
r = Usuario.objects.create_user("rrhh1", password="123", rol="rrhh")



Funcionalidades principales

Paciente: crear cita, ver citas.
Doctor: ver citas, marcar como atendidas, ver historial del paciente.
RRHH: gestionar horarios de doctores.


# Ejecutar
```bash
python manage.py runserver
```


