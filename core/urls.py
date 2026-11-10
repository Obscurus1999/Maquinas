from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogo_maquinaria, name='catalogo_maquinaria'),
    path('maquinaria/nuevo/', views.crear_maquinaria, name='crear_maquinaria'),
    path('maquinaria/editar/<int:pk>/', views.editar_maquinaria, name='editar_maquinaria'),
    path('maquinaria/eliminar/<int:pk>/', views.eliminar_maquinaria, name='eliminar_maquinaria'),
    path('maquinaria/<slug:slug>/', views.detalle_maquinaria, name='detalle_maquinaria'),
    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:maquinaria_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:maquinaria_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/checkout/', views.procesar_checkout, name='procesar_checkout'),
    
    path('accounts/login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='catalogo_maquinaria'), name='logout'),
    path('accounts/registro/', views.registro_usuario, name='registro'),
    
]