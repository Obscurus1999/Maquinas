from django.urls import path
from apps.reservas.views import (
    agregar_a_reservas,
    eliminar_de_reservas,
    procesar_checkout,
    vaciar_reservas,
    ver_reservas,
)

app_name = 'reservas'

urlpatterns = [
    path('', ver_reservas, name='ver'),
    path('agregar/<int:maquinaria_id>/', agregar_a_reservas, name='agregar'),
    path('eliminar/<int:maquinaria_id>/', eliminar_de_reservas, name='eliminar'),
    path('vaciar/', vaciar_reservas, name='vaciar'),
    path('checkout/', procesar_checkout, name='checkout'),
]