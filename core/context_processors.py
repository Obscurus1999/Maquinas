def contador_carrito(request):
    """
    Inyecta la cantidad total de elementos en la canasta de arriendo 
    para mostrarlo globalmente en la barra de navegación.
    """
    carrito = request.session.get('carrito', {})
    cantidad_total = sum(item.get('dias', 0) for item in carrito.values()) # O puedes usar len(carrito) si prefieres contar equipos únicos
    
    # Si prefieres contar cuántos equipos distintos hay en la canasta:
    cantidad_equipos = len(carrito)
    
    return {
        'cantidad_en_carrito': cantidad_equipos
    }