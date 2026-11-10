from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MaquinariaForm, RegistroForm
from .models import DetalleOrden, Maquinaria, OrdenArriendo, TipoFaena


# Create your views here.

def es_staff(user):
    return user.is_authenticated and user.is_staff

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


@login_required
@user_passes_test(es_staff)
def crear_maquinaria(request):
    """
    Solo accesible para usuarios autenticados que pertenezcan al staff (is_staff=True).
    Si un usuario normal intenta entrar, será redirigido o recibirá un error de acceso denegado.
    """
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo_maquinaria')
    else:
        form = MaquinariaForm()
    return render(
        request,
        'core/form_maquinaria.html',
        {'form': form, 'accion': 'Registrar Nuevo Equipo'},
    )


@login_required
@user_passes_test(es_staff)
def editar_maquinaria(request, pk):
    """Solo accesible para administradores/staff."""
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, request.FILES, instance=maquinaria)
        if form.is_valid():
            
            form.save()
            
            return redirect('catalogo_maquinaria')
        
    else:
        form = MaquinariaForm(instance=maquinaria)
    return render(
        request,
        'core/form_maquinaria.html',
        {'form': form, 'accion': 'Modificar Equipo'},
    )


@login_required
@user_passes_test(es_staff)
def eliminar_maquinaria(request, pk):
    """Solo accesible para administradores/staff (Realiza baja lógica)."""
    maquinaria = get_object_or_404(Maquinaria, pk=pk)
    if request.method == 'POST':
        maquinaria.vigente = False
        maquinaria.save()
        return redirect('catalogo_maquinaria')
    return render(
        request, 'core/eliminar_maquinaria.html', {'maquinaria': maquinaria}
    )


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    subtotal_general = 0
    fianza_total = 0

    for key, item in carrito.items():
        subtotal_item = item['tarifa_diaria'] * item['dias']
        subtotal_general += subtotal_item
        fianza_total += item['fianza']

        items.append({
            'maquinaria_id': key,
            'nombre': item['nombre'],
            'codigo': item['codigo'],
            'dias': item['dias'],
            'tarifa_diaria': item['tarifa_diaria'],
            'subtotal': subtotal_item,
            'fianza': item['fianza'],
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
    if 'carrito' not in request.session:
        request.session['carrito'] = {}

    carrito = request.session['carrito']
    str_id = str(maquinaria_id)

    maquinaria = get_object_or_404(Maquinaria, id=maquinaria_id)

    # 🔴 Capturamos los días enviados por POST desde el formulario de la card
    try:
        dias_seleccionados = int(request.POST.get('dias', 1))
        if dias_seleccionados < 1:
            dias_seleccionados = 1
    except (ValueError, TypeError):
        dias_seleccionados = 1

    # Agregar o actualizar el producto con los días ingresados
    if str_id in carrito:
        carrito[str_id]['dias'] = dias_seleccionados  # Reemplaza o actualiza los días
    else:
        carrito[str_id] = {
            'nombre': maquinaria.nombre,
            'codigo': getattr(maquinaria, 'codigo', ''),
            'tarifa_diaria': float(maquinaria.tarifa_diaria),
            'fianza': float(getattr(maquinaria, 'fianza', 0)),
            'dias': dias_seleccionados,
        }

    request.session.modified = True
    messages.success(request, f"¡'{maquinaria.nombre}' agregado a la canasta ({dias_seleccionados} días)!")
    return redirect(request.META.get('HTTP_REFERER') or 'catalogo_maquinaria')


def eliminar_del_carrito(request, maquinaria_id):
    carrito = request.session.get('carrito', {})
    str_id = str(maquinaria_id)
    if str_id in carrito:
        del carrito[str_id]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')


def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        request.session.modified = True
        
    return redirect('ver_carrito')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save() # El formulario se encarga del usuario, la señal y el perfil de forma atómica
            return redirect('login')
    else:
        form = RegistroForm()
        
    return render(request, 'core/registro.html', {'form': form})


@login_required
def procesar_checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, 'Tu canasta está vacía.')
        return redirect('ver_carrito')

    subtotal_general = Decimal('0')
    fianza_total = Decimal('0')

    for item in carrito.values():
        t = Decimal(str(item['tarifa_diaria']))
        f = Decimal(str(item['fianza']))
        d = int(item['dias'])

        item['subtotal'] = t * d
        subtotal_general += t * d
        fianza_total += f

    iva = subtotal_general * Decimal('0.19')
    total_final = subtotal_general + iva + fianza_total

    if request.method == 'POST':
        orden = OrdenArriendo.objects.create(
            user=request.user,
            subtotal=subtotal_general,
            iva=iva,
            fianza_total=fianza_total,
            total_final=total_final,
            estado='Pendiente',
        )

        for key, item in carrito.items():
            maquinaria_obj = Maquinaria.objects.filter(id=key).first()
            t = Decimal(str(item['tarifa_diaria']))
            d = int(item['dias'])

            DetalleOrden.objects.create(
                orden=orden,
                maquinaria=maquinaria_obj,
                nombre_equipo=item['nombre'],
                codigo_equipo=item['codigo'],
                tarifa_diaria=t,
                dias=d,
                subtotal_item=t * d,
            )

        del request.session['carrito']
        messages.success(
            request, f'¡Solicitud de arriendo #{orden.id} generada con éxito!'
        )
        return redirect('catalogo_maquinaria')

    context = {
        'carrito': carrito,
        'subtotal_general': subtotal_general,
        'iva': iva,
        'fianza_total': fianza_total,
        'total_final': total_final,
    }
    return render(request, 'core/checkout.html', context)