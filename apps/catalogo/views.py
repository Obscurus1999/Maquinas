from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MaquinariaForm
from .models import Maquinaria, TipoFaena


def es_staff(user):
    return user.is_authenticated and user.is_staff


def catalogo_maquinaria(request):
    query = request.GET.get('q', '')
    tipo_id = request.GET.get('tipo', '')
    orden = request.GET.get('orden', '')
    
    maquinarias = Maquinaria.objects.filter(vigente=True).select_related('tipo_faena')

    if query:
        maquinarias = maquinarias.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if tipo_id:
        maquinarias = maquinarias.filter(tipo_faena_id=tipo_id)

    if orden == 'precio_asc':
        maquinarias = maquinarias.order_by('tarifa_diaria')
    elif orden == 'precio_desc':
        maquinarias = maquinarias.order_by('-tarifa_diaria')
    elif orden == 'nombre':
        maquinarias = maquinarias.order_by('nombre')
    else:
        maquinarias = maquinarias.order_by('-id')

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
    return render(request, 'catalogo/maquinaria_lista.html', context)


def detalle_maquinaria(request, slug):
    maquinaria = get_object_or_404(Maquinaria, slug=slug, vigente=True)
    return render(request, 'catalogo/maquinaria_detalle.html', {'maquinaria': maquinaria})


@login_required
@user_passes_test(es_staff)
def crear_maquinaria(request):
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo:lista')
    else:
        form = MaquinariaForm()
    return render(
        request,
        'catalogo/maquinaria_form.html',
        {'form': form, 'accion': 'Registrar Nuevo Equipo'},
    )


@login_required
@user_passes_test(es_staff)
def editar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, request.FILES, instance=maquinaria)
        if form.is_valid():
            form.save()
            return redirect('catalogo:lista')
    else:
        form = MaquinariaForm(instance=maquinaria)
    return render(
        request,
        'catalogo/maquinaria_form.html',
        {'form': form, 'accion': 'Modificar Equipo'},
    )


@login_required
@user_passes_test(es_staff)
def eliminar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        maquinaria.vigente = False
        maquinaria.save()
        return redirect('catalogo:gestion')
    return render(
        request, 'catalogo/maquinaria_confirmar_eliminar.html', {'maquinaria': maquinaria}
    )
    
@login_required
@user_passes_test(es_staff, login_url='catalogo:lista')
def gestion_maquinaria(request):
    query = request.GET.get('q', '').strip()
    
    # Traemos todas las maquinarias (incluyendo las no vigentes si el admin necesita administrarlas, o ajusta a vigente=True si prefieres)
    maquinarias = Maquinaria.objects.all().select_related('tipo_faena')

    if query:
        maquinarias = maquinarias.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginador = Paginator(maquinarias.order_by('-fecha_creacion'), 10)
    pagina = paginador.get_page(request.GET.get('page'))

    context = {
        'maquinarias': pagina,
        'query': query,
    }
    return render(request, 'catalogo/gestion_maquinaria.html', context)    