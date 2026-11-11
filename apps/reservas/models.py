from django.contrib.auth.models import User
from django.db import models
from apps.catalogo.models import Maquinaria


class OrdenArriendo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cliente")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Subtotal")
    iva = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="IVA (19%)")
    fianza_total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Fianza Total")
    total_final = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Total Final")
    estado = models.CharField(max_length=50, default="Pendiente de Aprobación", verbose_name="Estado")

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"
    
class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenArriendo, related_name='detalles', on_delete=models.CASCADE)
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.SET_NULL, null=True, verbose_name="Maquinaria")
    nombre_equipo = models.CharField(max_length=150, verbose_name="Nombre Equipo")
    codigo_equipo = models.CharField(max_length=50, verbose_name="Código")
    tarifa_diaria = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Tarifa Diaria")
    dias = models.PositiveIntegerField(verbose_name="Días")
    subtotal_item = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Subtotal Ítem")

    def __str__(self):
        return f"{self.dias}x {self.nombre_equipo} (Orden #{self.orden.id})"