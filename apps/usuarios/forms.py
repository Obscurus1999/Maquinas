from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


class RegistroForm(UserCreationForm):
    rut = forms.CharField(max_length=12, required=True, label="RUT")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Actualiza o crea el perfil asociado
            Perfil.objects.update_or_create(
                user=user,
                defaults={
                    'rut': self.cleaned_data.get('rut'),
                    'telefono': self.cleaned_data.get('telefono'),
                }
            )
        return user