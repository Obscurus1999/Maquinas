from django import forms
from .models import Maquinaria

class MaquinariaForm(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = [
            'codigo', 'nombre', 'tipo_faena', 'descripcion', 
            'tarifa_diaria', 'fianza', 'capacidad_carga', 
            'estado', 'imagen', 'vigente'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_faena': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tarifa_diaria': forms.NumberInput(attrs={'class': 'form-control'}),
            'fianza': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad_carga': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'vigente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Validación clean_() para el identificador único
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        qs = Maquinaria.objects.filter(codigo=codigo)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe otro equipo registrado con este código identificador.")
        return codigo

    # Validación clean_() para tarifa no negativa
    def clean_tarifa_diaria(self):
        tarifa = self.cleaned_data.get('tarifa_diaria')
        if tarifa is not None and tarifa < 0:
            raise forms.ValidationError("La tarifa diaria no puede ser un valor negativo.")
        return tarifa

    # Validación clean_() para fianza no negativa
    def clean_fianza(self):
        fianza = self.cleaned_data.get('fianza')
        if fianza is not None and fianza < 0:
            raise forms.ValidationError("La fianza/garantía no puede ser un valor negativo.")
        return fianza