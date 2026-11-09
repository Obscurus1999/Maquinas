from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Maquinaria, TipoFaena
from .forms import MaquinariaForm

# Create your views here.

def catalogo_maquinaria(request):
    query = request.GET.get('q', '')
    tipo_id = request.GET.get('tipo', '')
    orden = request.GET.get('orden', '')
    # Obtenemos toda la maquinaria vigente para mostrarla en el catálogo
    maquinarias = Maquinaria.objects.filter(vigente=True).select_related('tipo_faena')
    
    # Búsqueda multi-campo simultánea con objeto Q (título, código y descripción)
    if query:
        maquinarias = maquinarias.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    # Filtro por entidad de contexto (TipoFaena)
    if tipo_id:
        maquinarias = maquinarias.filter(tipo_faena_id=tipo_id)

    # Ordenamiento de resultados
    if orden == 'precio_asc':
        maquinarias = maquinarias.order_by('tarifa_diaria')
    elif orden == 'precio_desc':
        maquinarias = maquinarias.order_by('-tarifa_diaria')
    elif orden == 'nombre':
        maquinarias = maquinarias.order_by('nombre')
    else:
        maquinarias = maquinarias.order_by('-id')

    # Paginación con Paginator 
    paginator = Paginator(maquinarias, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tipos_faena = TipoFaena.objects.filter(activa=True)

    context = {
        'page_obj': page_obj,
        'tipos_faena': tipos_faena,
        'query': query,
        'tipo_seleccionado': int(tipo_id) if tipo_id else '',
        'orden': orden,
    }
    return render(request, 'core/catalogo.html', context)

def detalle_maquinaria(request, slug):
    maquinaria = get_object_or_404(Maquinaria, slug=slug, vigente=True)
    return render(request, 'core/detalle.html', {'maquinaria': maquinaria})

def crear_maquinaria(request):
    if request.method == 'POST':
        # enctype='multipart/form-data' se gestiona automáticamente con request.FILES
        form = MaquinariaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo_maquinaria')
    else:
        form = MaquinariaForm()
    return render(request, 'core/form_maquinaria.html', {'form': form, 'accion': 'Registrar Nuevo Equipo'})

def editar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, request.FILES, instance=maquinaria)
        if form.is_valid():
            form.save()
            return redirect('catalogo_maquinaria')
    else:
        form = MaquinariaForm(instance=maquinaria)
    return render(request, 'core/form_maquinaria.html', {'form': form, 'accion': 'Modificar Equipo'})

def eliminar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        # Eliminación controlada (Baja lógica cambiando vigente a False)
        maquinaria.vigente = False
        maquinaria.save()
        return redirect('catalogo_maquinaria')
    return render(request, 'core/eliminar_maquinaria.html', {'maquinaria': maquinaria})

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    subtotal_general = 0
    fianza_total = 0

    for maquinaria_id, item_data in carrito.items():
        maquinaria = Maquinaria.objects.get(id=maquinaria_id)
        dias = item_data['dias']
        subtotal_item = float(maquinaria.tarifa_diaria) * dias
        fianza_item = float(maquinaria.fianza)
        
        subtotal_general += subtotal_item
        fianza_total += fianza_item

        items.append({
            'maquinaria': maquinaria,
            'dias': dias,
            'subtotal': subtotal_item,
            'fianza': fianza_item
        })

    iva = subtotal_general * 0.19
    total_general = subtotal_general + iva + fianza_total

    context = {
        'items': items,
        'subtotal_general': subtotal_general,
        'fianza_total': fianza_total,
        'iva': iva,
        'total_general': total_general,
    }
    return render(request, 'core/carrito.html', context)

def agregar_al_carrito(request, maquinaria_id):
    maquinaria = get_object_or_404(Maquinaria, id=maquinaria_id)
    carrito = request.session.get('carrito', {})
    
    dias = int(request.POST.get('dias', 1))
    if dias < 1:
        dias = 1

    str_id = str(maquinaria_id)
    if str_id in carrito:
        carrito[str_id]['dias'] += dias
    else:
        carrito[str_id] = {
            'dias': dias,
        }

    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, maquinaria_id):
    carrito = request.session.get('carrito', {})
    str_id = str(maquinaria_id)
    if str_id in carrito:
        del carrito[str_id]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')