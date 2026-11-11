from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name="RUT")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    rol_institucional = models.CharField(max_length=50, default="Cliente", verbose_name="Rol Institucional")

    def __str__(self):
        return f"{self.user.username} - {self.rut}"