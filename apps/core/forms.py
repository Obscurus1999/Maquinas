from django import forms
from .models import Maquinaria
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

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
    
class RegistroForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}), label="RUT")
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Teléfono")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    @transaction.atomic
    def save(self, commit=True):
        # 1. Creamos el usuario base
        user = super().save(commit=commit)
        
        if commit:
            # 2. Creamos el perfil usando get_or_create para blindarnos 
            # ante cualquier duplicado fantasma en la base de datos
            Perfil.objects.get_or_create(
                user=user,
                defaults={'rut': self.cleaned_data.get('rut')}
            )
        return user