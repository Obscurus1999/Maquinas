from django.urls import path
from apps.catalogo.views import (
    catalogo_maquinaria,
    crear_maquinaria,
    detalle_maquinaria,
    editar_maquinaria,
    eliminar_maquinaria,
)

app_name = 'catalogo'

urlpatterns = [
    path('', catalogo_maquinaria, name='lista'),
    path('detalle/<slug:slug>/', detalle_maquinaria, name='detalle'),
    path('nuevo/', crear_maquinaria, name='crear'),
    path('editar/<int:pk>/', editar_maquinaria, name='editar'),
    path('eliminar/<int:pk>/', eliminar_maquinaria, name='eliminar'),
]