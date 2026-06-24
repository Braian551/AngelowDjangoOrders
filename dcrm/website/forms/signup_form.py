# Formulario de registro

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Formulario personalizado para registrar usuarios en el sistema.

    Centraliza etiquetas y mensajes en español para evitar errores genéricos
    como "This field is required." en las pantallas de autenticación.
    """

    # Campos adicionales al formulario base de Django para completar el perfil inicial.
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}
        ),
        error_messages={
            'required': 'Debes ingresar un correo electrónico.',
            'invalid': 'Ingresa un correo electrónico válido.',
        },
    )

    first_name = forms.CharField(
        label='Nombre',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nombre'}
        ),
        error_messages={
            'required': 'Debes ingresar tu nombre.',
        },
    )

    last_name = forms.CharField(
        label='Apellido',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Apellido'}
        ),
        error_messages={
            'required': 'Debes ingresar tu apellido.',
        },
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
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

    def __init__(self, *args, **kwargs):
        """Ajusta etiquetas, ayudas y clases CSS de los campos heredados."""
        super().__init__(*args, **kwargs)

        # Los campos heredados no se pueden personalizar arriba, por eso se ajustan aquí.
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre de usuario'}
        )
        self.fields['username'].label = 'Usuario'
        self.fields['username'].error_messages.update(
            {
                'required': 'Debes ingresar un nombre de usuario.',
                'unique': 'Ya existe un usuario con ese nombre.',
            }
        )
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
            '</small></span>'
        )

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña'}
        )
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].error_messages.update(
            {
                'required': 'Debes ingresar una contraseña.',
            }
        )
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
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].error_messages.update(
            {
                'required': 'Debes confirmar la contraseña.',
            }
        )
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Ingrese la misma contraseña que antes, para verificación.'
            '</small></span>'
        )

    def clean_password2(self):
        """
        Valida que ambas contraseñas coincidan con un mensaje claro en español.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return password2
