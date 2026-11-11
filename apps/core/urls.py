from django.urls import path
from apps.core.views import inicio, nosotros

app_name = 'core'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('nosotros/', nosotros, name='nosotros'),
]