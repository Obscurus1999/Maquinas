from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


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

    @property
    def tarifa_formateada(self):
        return f"${self.tarifa_diaria:,.0f}".replace(",", ".")

    @property
    def fianza_formateada(self):
        return f"${self.fianza:,.0f}".replace(",", ".")

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