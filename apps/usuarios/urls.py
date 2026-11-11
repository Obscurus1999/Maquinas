from django.contrib.auth import views as auth_views
from django.urls import path
from apps.usuarios.views import registro_usuario

app_name = 'usuarios'

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='catalogo:lista'), name='logout'),
]