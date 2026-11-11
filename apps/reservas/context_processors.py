def contador_reservas(request):
    """
    Inyecta la cantidad de equipos en la lista de reserva o cotización
    para mostrarlo globalmente en la barra de navegación.
    """
    carrito = request.session.get('carrito', {})
    
    # Cantidad de equipos distintos agregados a la reserva
    cantidad_equipos = len(carrito)
    
    return {
        'cantidad_en_reservas': cantidad_equipos
    }