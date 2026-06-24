# Formulario de registro

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Formulario personalizado para registrar usuarios en el sistema."""

    # Campos adicionales al formulario base de Django para completar el perfil inicial.
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}
        ),
    )

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nombre'}
        ),
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Apellido'}
        ),
    )

    class Meta:
        model = User
        # Define el orden en que los campos aparecen al renderizar `form.as_p`.
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        """Ajusta etiquetas, ayudas y clases CSS de los campos heredados."""
        super().__init__(*args, **kwargs)

        # Los campos heredados no se pueden personalizar arriba, por eso se ajustan aquí.
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre de usuario'}
        )
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
            '</small></span>'
        )

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña'}
        )
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted">'
            '<li>Tu contraseña no puede ser demasiado similar a tu otra información personal.</li>'
            '<li>Tu contraseña debe contener al menos 8 caracteres.</li>'
            '<li>Tu contraseña no puede ser una contraseña común.</li>'
            '<li>Tu contraseña no puede ser completamente numérica.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirmar contraseña'}
        )
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Ingrese la misma contraseña que antes, para verificación.'
            '</small></span>'
        )
