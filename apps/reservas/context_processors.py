def contador_reservas(request):
    """
    Inyecta la cantidad de equipos en la lista de reserva o cotización
    para mostrarlo globalmente en la barra de navegación.
    """
    reserva = request.session.get('reserva', {})
    
    # Cantidad de equipos distintos agregados a la reserva
    cantidad_equipos = len(reserva)
    
    return {
        'cantidad_en_reservas': cantidad_equipos
    }