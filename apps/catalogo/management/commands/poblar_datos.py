from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import TipoFaena, Maquinaria
from apps.usuarios.models import Perfil

class Command(BaseCommand):
    help = 'Pobla la base de datos con tipos de faena, maquinaria de carga, usuarios y perfiles.'

    def handle(self, *args, **kwargs):
        # Limpiar registros previos para evitar duplicados
        Maquinaria.objects.all().delete()
        TipoFaena.objects.all().delete()

        # 1. Crear 4 Tipos de Faena (Clasificadores)
        tf1 = TipoFaena.objects.create(nombre="Construcción Edificación", descripcion="Obras civiles, edificios en altura y fundaciones.")
        tf2 = TipoFaena.objects.create(nombre="Logística y Bodegaje", descripcion="Centros de distribución y manipulación de carga paletizada.")
        tf3 = TipoFaena.objects.create(nombre="Minería y Gran Minería", descripcion="Operaciones pesadas de alto rendimiento y autonomía.")
        tf4 = TipoFaena.objects.create(nombre="Obras Viales", descripcion="Movimiento de tierra y preparación de caminos.")

        # 2. Crear 8 Maquinarias de Carga (Entidades principales)
        Maquinaria.objects.create(codigo="MQ-01", nombre="Grúa Horquilla 3T", tipo_faena=tf2, descripcion="Combustión gas/bencina, mástil doble.", tarifa_diaria=45000, fianza=150000, capacidad_carga="3.0 Toneladas", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-02", nombre="Apilador Eléctrico", tipo_faena=tf2, descripcion="Ideal para pasillos angostos en bodegas.", tarifa_diaria=35000, fianza=120000, capacidad_carga="1.8 Toneladas", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-03", nombre="Camión Pluma 5T", tipo_faena=tf1, descripcion="Camión con brazo articulado incorporado.", tarifa_diaria=180000, fianza=500000, capacidad_carga="5.0 Toneladas Pluma", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-04", nombre="Retroexcavadora 4x4", tipo_faena=tf4, descripcion="Versátil para excavación y carga frontal.", tarifa_diaria=120000, fianza=350000, capacidad_carga="Cuchara 1.1 m3", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-05", nombre="Manipulador Telescópico", tipo_faena=tf1, descripcion="Alcance en altura para materiales de construcción.", tarifa_diaria=160000, fianza=450000, capacidad_carga="3.5 Toneladas", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-06", nombre="Minicargador Frontal", tipo_faena=tf4, descripcion="Compacto para espacios reducidos.", tarifa_diaria=85000, fianza=250000, capacidad_carga="850 kg", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-07", nombre="Excavadora Hidráulica 20T", tipo_faena=tf3, descripcion="Alto rendimiento para faenas mineras masivas.", tarifa_diaria=250000, fianza=800000, capacidad_carga="Balde 1.2 m3", estado="DISPONIBLE")
        Maquinaria.objects.create(codigo="MQ-08", nombre="Transpaleta Eléctrica", tipo_faena=tf2, descripcion="Traslado rápido de pallets a nivel de piso.", tarifa_diaria=25000, fianza=80000, capacidad_carga="2.0 Toneladas", estado="DISPONIBLE")

        # 3. Crear usuarios de prueba y sus perfiles obligatorios
        admin_user, created = User.objects.get_or_create(
            username="admin", 
            defaults={"email": "admin@maquinaria.cl", "is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()

        # Crear o actualizar perfil del admin
        Perfil.objects.get_or_create(
            user=admin_user, 
            defaults={
                "rut": "12.345.678-9", 
                "telefono": "+56912345678", 
                "rol_institucional": "Administrador"
            }
        )

        operador_user, created = User.objects.get_or_create(
            username="operador", 
            defaults={"email": "operador@maquinaria.cl"}
        )
        if created:
            operador_user.set_password("user123")
            operador_user.save()

        # Crear o actualizar perfil del operador
        Perfil.objects.get_or_create(
            user=operador_user, 
            defaults={
                "rut": "98.765.432-1", 
                "telefono": "+56987654321", 
                "rol_institucional": "Operador"
            }
        )
        
        self.stdout.write(self.style.SUCCESS("¡Base de datos poblada exitosamente con faenas, maquinaria, usuarios y perfiles!"))