from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record


class SignUpForm(UserCreationForm):
    """Formulario personalizado para registrar usuarios en el sistema."""

    # Campos adicionales del usuario con clases de Bootstrap para mantener el estilo visual.
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}
        ),
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
    )

    class Meta:
        # Se usa el modelo User nativo de Django para guardar la cuenta.
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """Ajusta etiquetas, ayudas y clases CSS de los campos heredados."""
        super().__init__(*args, **kwargs)

        # Nombre de usuario.
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre de usuario'}
        )
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
            '</small></span>'
        )

        # Contraseña principal.
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

        # Confirmación de contraseña.
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirmar contraseña'}
        )
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Ingrese la misma contraseña que antes, para verificación.'
            '</small></span>'
        )


class RecordForm(forms.ModelForm):
    """Formulario para crear o actualizar la información de un cliente."""

    # Campos del cliente con placeholders en español y estilos de Bootstrap.
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'}
        ),
    )
    phone_number = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Número de teléfono', 'class': 'form-control'}
        ),
    )
    address = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Dirección', 'class': 'form-control'}),
    )
    city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Ciudad', 'class': 'form-control'}),
    )
    state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Estado', 'class': 'form-control'}),
    )
    zip_code = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Código postal', 'class': 'form-control'}),
    )

    class Meta:
        # Relaciona el formulario con el modelo Record y limita los campos editables.
        model = Record
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'city',
            'state',
            'zip_code',
        )
