#

from django import forms

from website.models import Record


class RecordForm(forms.ModelForm):
    """Formulario para crear o actualizar la información de un cliente."""

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombre', 'class': 'form-control'}
        ),
    )

    last_name = forms.CharField(
        label='',
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
        widget=forms.TextInput(
            attrs={'placeholder': 'Número de teléfono', 'class': 'form-control'}
        ),
    )

    address = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Dirección', 'class': 'form-control'}
        ),
    )

    city = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Ciudad', 'class': 'form-control'}
        ),
    )

    state = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Estado', 'class': 'form-control'}
        ),
    )

    zip_code = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Código postal', 'class': 'form-control'}
        ),
    )

    class Meta:
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