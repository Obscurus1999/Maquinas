# 🏗️ Maquinaria SpA - Sistema de Arriendo de Maquinaria de Carga

**Nombre de la Organización o Plataforma:** Maquinaria SpA  
**Modelo de Negocio / Giro:** Arriendo de flotas y maquinaria pesada de carga para faenas.  
**Integrantes del Equipo:** Emmanuel Eusebio Toro Valladares - 20078585-1  
**Entidad de Contexto / Agrupación (ORM):** `TipoFaena` (Construcción, Logística, Minería, Obras Viales)  
**Entidad Principal Gestionable (ORM):** `Maquinaria` (Grúas, camiones pluma, apiladores, etc.)  
**Propósito de la Sesión (request.session):** Canasta de arriendo por días con cálculo de subtotal, fianza/garantía e IVA (19%).

📝 Bitácora de Prompts - Módulo 3: Uso Técnico y Ético de IA
Caso 1: Optimización de Consultas ORM con select_related
Prompt utilizado:

"Tengo un modelo de Maquinaria relacionado con Categorías mediante ForeignKey en Django. Al listar una gran cantidad de máquinas en el catálogo, noto múltiples consultas repetitivas a la base de datos (problema N+1). ¿Cómo puedo optimizar la consulta en mi vista catalogo_maquinaria usando Django ORM y select_related?"

Respuesta técnica de la IA:

La IA explicó el concepto del problema N+1 y recomendó modificar el queryset en la vista utilizando .select_related('categoria') antes de pasar los objetos al template, lo que realiza un único SQL JOIN en lugar de una consulta por cada iteración de máquina.

Adaptación aplicada:

Se aplicó directamente en la vista del catálogo: maquinarias = Maquinaria.objects.filter(vigente=True).select_related('categoria'), reduciendo drásticamente el tiempo de carga de las tarjetas en la interfaz.

Caso 2: Implementación de Señales (Signals) para Creación Automática de Perfiles (Perfil)
Prompt utilizado:

"Necesito extender el modelo User de Django con un modelo Perfil (que guarde RUT, teléfono, etc.) mediante una relación OneToOneField. ¿Cómo puedo asegurar que cada vez que se registre un usuario nuevo se cree automáticamente su perfil sin intervención manual en las vistas?"

Respuesta técnica de la IA:

La IA sugirió utilizar Django Signals (post_save) conectadas al modelo User. Proporcionó un ejemplo de estructura creando un archivo signals.py y configurándolo dentro de la clase AppConfig en apps.py mediante el método ready().

Adaptación aplicada:

Se creó el archivo core/signals.py con el decorador @receiver(post_save, sender=User) para instanciar el Perfil automáticamente al registrar usuarios, y se complementó con un script de consola para migrar los usuarios antiguos que no lo poseían.

Caso 3: Seguridad y Restricción de Rutas con Decoradores en Django
Prompt utilizado:

"¿Cómo puedo proteger las vistas de creación, edición y eliminación de maquinaria en Django para que solo los usuarios administradores (staff) puedan acceder a ellas, y qué debo hacer si un usuario común intenta ingresar por URL?"

Respuesta técnica de la IA:

La IA indicó el uso combinado de los decoradores @login_required y un filtro personalizado con @user_passes_test(lambda u: u.is_staff), explicando que redirigen automáticamente al login configurado en el settings.py en caso de no cumplir la validación.

Adaptación aplicada:

Se implementó una función auxiliar booleana es_staff(user) combinada con los decoradores en las vistas administrativas (crear_maquinaria, editar_maquinaria, eliminar_maquinaria) para salvaguardar los endpoints del sistema de arriendos.
