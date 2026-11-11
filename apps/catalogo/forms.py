from django import forms
from .models import Maquinaria


class MaquinariaForm(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = [
            'codigo',
            'nombre',
            'tipo_faena',
            'descripcion',
            'tarifa_diaria',
            'fianza',
            'capacidad_carga',
            'estado',
            'imagen',
            'vigente',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }