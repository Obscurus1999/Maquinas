from django.contrib import admin
from .models import TipoFaena, Maquinaria

admin.site.site_header = 'Maquinaria SpA - Panel de Control'
admin.site.site_title = 'Maquinaria SpA Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'

@admin.register(TipoFaena)
class TipoFaenaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activa',)
    list_editable = ('activa',)


@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo_faena', 'tarifa_diaria', 'fianza', 'estado', 'vigente')
    list_filter = ('estado', 'tipo_faena', 'vigente')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_editable = ('tarifa_diaria', 'estado', 'vigente')
    readonly_fields = ('slug',)
    
    # Organización visual de los campos en el formulario de edición
    fieldsets = (
        ('Identificación del Equipo', {
            'fields': ('codigo', 'nombre', 'slug', 'tipo_faena')
        }),
        ('Detalles Financieros y Técnicos', {
            'fields': ('tarifa_diaria', 'fianza', 'capacidad_carga', 'descripcion')
        }),
        ('Estado Operativo y Multimedia', {
            'fields': ('estado', 'vigente', 'imagen')
        }),
    )

    # Acciones personalizadas en lote para la administración de flotas
    actions = ['marcar_como_disponible', 'marcar_como_suspendido']

    @admin.action(description="Marcar equipos seleccionados como DISPONIBLE")
    def marcar_como_disponible(self, request, queryset):
        updated = queryset.update(estado='DISPONIBLE')
        self.message_user(request, f"¡Éxito! {updated} equipos fueron marcados como disponibles.")

    @admin.action(description="Marcar equipos seleccionados como SUSPENDIDO")
    def marcar_como_suspendido(self, request, queryset):
        updated = queryset.update(estado='SUSPENDIDO')
        self.message_user(request, f"¡Atención! {updated} equipos fueron suspendidos de la flota.")