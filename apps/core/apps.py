from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Núcleo del Sitio'
    
    def ready(self):
        # Importamos las señales para que Django las registre al arrancar
        import apps.core.signals  # noqa