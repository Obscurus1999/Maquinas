from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.db.models.signals import post_save



# Create your models here.
class TipoFaena(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Faena")
    descripcion = models.TextField(verbose_name="Descripción del Sector")
    activa = models.BooleanField(default=True, verbose_name="Faena Vigente")

    def __str__(self):
        return self.nombre

class Maquinaria(models.Model):
    ESTADOS_OPERATIVOS = [
        ('DISPONIBLE', 'Disponible'),
        ('ARRENDADO', 'Arrendado'),
        ('MANTENCION', 'En Mantención'),
        ('SUSPENDIDO', 'Suspendido'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código de Inventario")
    nombre = models.CharField(max_length=150, verbose_name="Modelo / Equipo")
    slug = models.SlugField(unique=True, blank=True, max_length=160)
    tipo_faena = models.ForeignKey(TipoFaena, on_delete=models.PROTECT, verbose_name="Tipo de Faena")
    descripcion = models.TextField(verbose_name="Especificaciones Técnicas")
    tarifa_diaria = models.DecimalField(
        max_digits=10, decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        verbose_name="Tarifa Diaria (CLP)"
    )
    fianza = models.DecimalField(
        max_digits=10, decimal_places=2, 
        validators=[MinValueValidator(0.00)], 
        verbose_name="Fianza / Garantía (CLP)"
    )
    capacidad_carga = models.CharField(max_length=50, verbose_name="Capacidad de Carga")
    estado = models.CharField(max_length=20, choices=ESTADOS_OPERATIVOS, default='DISPONIBLE', verbose_name="Estado Operativo")
    imagen = models.ImageField(upload_to='maquinaria/', blank=True, null=True, verbose_name="Fotografía")
    vigente = models.BooleanField(default=True, verbose_name="Vigente en Catálogo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Maquinarias"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    # Propiedad para formatear la tarifa diaria en formato chileno (ej: $45.000)
    @property
    def tarifa_formateada(self):
        return f"${self.tarifa_diaria:,.0f}".replace(",", ".")

    # Propiedad para formatear la fianza en formato chileno
    @property
    def fianza_formateada(self):
        return f"${self.fianza:,.0f}".replace(",", ".")

    # Generación automática de slugs únicos
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while Maquinaria.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)
            
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name="RUT")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    rol_institucional = models.CharField(max_length=50, default="Cliente", verbose_name="Rol Institucional")

    def __str__(self):
        return f"{self.user.username} - {self.rut}"
    
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
        return f"{self.cantidad_dias}x {self.nombre_equipo} (Orden #{self.orden.id})"
    
    