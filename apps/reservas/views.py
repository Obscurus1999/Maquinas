from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.catalogo.models import Maquinaria
from .models import DetalleOrden, OrdenArriendo


def agregar_a_reservas(request, maquinaria_id):
    if 'reserva' not in request.session:
        request.session['reserva'] = {}

    reserva = request.session['reserva']
    str_id = str(maquinaria_id)
    maquinaria = get_object_or_404(Maquinaria, id=maquinaria_id)

    try:
        dias_seleccionados = int(request.POST.get('dias', 1))
        if dias_seleccionados < 1:
            dias_seleccionados = 1
    except (ValueError, TypeError):
        dias_seleccionados = 1

    if str_id in reserva:
        reserva[str_id]['dias'] = dias_seleccionados
    else:
        reserva[str_id] = {
            'nombre': maquinaria.nombre,
            'codigo': getattr(maquinaria, 'codigo', ''),
            'tarifa_diaria': float(maquinaria.tarifa_diaria),
            'fianza': float(getattr(maquinaria, 'fianza', 0)),
            'dias': dias_seleccionados,
        }

    request.session.modified = True
    messages.success(request, f"¡'{maquinaria.nombre}' agregado a tu reserva ({dias_seleccionados} días)!")
    return redirect(request.META.get('HTTP_REFERER') or 'catalogo:lista')


def ver_reservas(request):
    reserva = request.session.get('reserva', {})
    items = []
    subtotal_general = Decimal('0')
    fianza_total = Decimal('0')

    for key, item in reserva.items():
        t = Decimal(str(item['tarifa_diaria']))
        f = Decimal(str(item['fianza']))
        d = int(item['dias'])
        subtotal_item = t * d
        
        subtotal_general += subtotal_item
        fianza_total += f

        items.append({
            'maquinaria_id': key,
            'nombre': item['nombre'],
            'codigo': item['codigo'],
            'dias': d,
            'tarifa_diaria': t,
            'subtotal': subtotal_item,
            'fianza': f,
        })

    iva = subtotal_general * Decimal('0.19')
    total_general = subtotal_general + iva + fianza_total

    context = {
        'items': items,
        'subtotal_general': subtotal_general,
        'fianza_total': fianza_total,
        'iva': iva,
        'total_general': total_general,
    }
    return render(request, 'reservas/reservas.html', context)


def eliminar_de_reservas(request, maquinaria_id):
    reserva = request.session.get('reserva', {})
    str_id = str(maquinaria_id)
    if str_id in reserva:
        del reserva[str_id]
        request.session['reserva'] = reserva
        request.session.modified = True
    return redirect('reservas:ver')


def vaciar_reservas(request):
    if 'reserva' in request.session:
        del request.session['reserva']
        request.session.modified = True
    return redirect('reservas:ver')


@login_required
def procesar_checkout(request):
    reserva = request.session.get('reserva', {})
    if not reserva:
        messages.warning(request, 'Tu lista de reserva está vacía.')
        return redirect('reservas:ver')

    subtotal_general = Decimal('0')
    fianza_total = Decimal('0')

    for item in reserva.values():
        t = Decimal(str(item['tarifa_diaria']))
        f = Decimal(str(item['fianza']))
        d = int(item['dias'])
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

        for key, item in reserva.items():
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

            if maquinaria_obj:
                maquinaria_obj.vigente = False             # Lo oculta del catálogo público
                maquinaria_obj.estado = 'ARRENDADO' # cambia el estado
                maquinaria_obj.save()
            
        del request.session['reserva']
        request.session.modified = True
        messages.success(request, f'¡Solicitud de arriendo #{orden.id} generada con éxito!')
        return redirect('catalogo:lista')

    context = {
        'reserva': reserva,
        'subtotal_general': subtotal_general,
        'iva': iva,
        'fianza_total': fianza_total,
        'total_final': total_final,
    }
    return render(request, 'reservas/checkout_exito.html', context)


def contador_reservas(request):
    reserva = request.session.get('reserva', {})
    cantidad_equipos = len(reserva)
    return {
        'cantidad_en_reservas': cantidad_equipos
    }