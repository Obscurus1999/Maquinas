from django.shortcuts import render
from apps.catalogo.models import Maquinaria, TipoFaena


def inicio(request):
    """
    Vista para la página de bienvenida o inicio del sitio de arriendo.
    Opcionalmente muestra una selección de maquinaria destacada o los tipos de faena disponibles.
    """
    maquinarias_destacadas = Maquinaria.objects.filter(vigente=True)[:4]
    tipos_faena = TipoFaena.objects.filter(activa=True)
    
    context = {
        'maquinarias_destacadas': maquinarias_destacadas,
        'tipos_faena': tipos_faena,
    }
    return render(request, 'core/index.html', context)


def nosotros(request):
    """
    Vista para la sección institucional o "Quiénes Somos" de la empresa de arriendo.
    """
    return render(request, 'core/nosotros.html')