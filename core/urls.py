from django.urls import path
from . import views

urlpatterns = [
    # Dejaremos esto listo para cuando configuremos las vistas del catálogo y CRUD
    path('', views.catalogo_maquinaria, name='catalogo_maquinaria'),
]