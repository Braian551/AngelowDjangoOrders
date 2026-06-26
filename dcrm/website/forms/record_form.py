"""Formulario para datos de clientes.

Patrón/convenio Django: ModelForm / Form Object.
Centraliza validaciones de entrada y renderizado básico de widgets Bootstrap.
"""

from django import forms
from django.core.validators import RegexValidator

from website.models import Record


name_validator = RegexValidator(
    regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
    message='Solo se permiten letras y espacios.',
)

phone_validator = RegexValidator(
    regex=r'^[0-9+\-\s]+$',
    message='Solo se permiten números, espacios y los caracteres + -.',
)

address_validator = RegexValidator(
    regex=r'^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s#.,-]+$',
    message='La dirección contiene caracteres no permitidos.',
)

zip_code_validator = RegexValidator(
    regex=r'^[A-Za-z0-9-]+$',
    message='El código postal solo puede contener letras, números y guion.',
)


class RecordForm(forms.ModelForm):
    """
    Formulario para crear o actualizar la información de un cliente.

    La vista solo pregunta si el formulario es válido; las reglas de campos
    y mensajes viven aquí para reducir duplicación.
    """

    # Se declaran los campos para controlar placeholders y clases Bootstrap desde Python.
    first_name = forms.CharField(
        label='',
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombre', 'class': 'form-control'}
        ),
    )

    last_name = forms.CharField(
        label='',
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Apellido', 'class': 'form-control'}
        ),
    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'}
        ),
    )

    phone_number = forms.CharField(
        label='',
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Número de teléfono', 'class': 'form-control'}
        ),
    )

    address = forms.CharField(
        label='',
        validators=[address_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Dirección', 'class': 'form-control'}
        ),
    )

    city = forms.CharField(
        label='',
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Ciudad', 'class': 'form-control'}
        ),
    )

    state = forms.CharField(
        label='',
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Estado', 'class': 'form-control'}
        ),
    )

    zip_code = forms.CharField(
        label='',
        validators=[zip_code_validator],
        widget=forms.TextInput(
            attrs={'placeholder': 'Código postal', 'class': 'form-control'}
        ),
    )

    class Meta:
        # Mantener esta lista explícita evita exponer campos no deseados en el formulario.
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
