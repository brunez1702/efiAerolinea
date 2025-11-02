from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reserva

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vuelo', 'asiento', 'pasajero']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['vuelo'].label = "Seleccionar vuelo"
        self.fields['asiento'].label = "Seleccionar asiento"
        self.fields['pasajero'].label = "Seleccionar pasajero"
