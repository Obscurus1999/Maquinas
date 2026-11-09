from django.shortcuts import render
from django.shortcuts import render
from .models import Maquinaria, TipoFaena

# Create your views here.

def catalogo_maquinaria(request):
    # Obtenemos toda la maquinaria vigente para mostrarla en el catálogo
    maquinarias = Maquinaria.objects.filter(vigente=True).select_related('tipo_faena')
    tipos_faena = TipoFaena.objects.filter(activa=True)
    
    context = {
        'maquinarias': maquinarias,
        'tipos_faena': tipos_faena,
    }
    return render(request, 'core/catalogo.html', context)