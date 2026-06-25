from decimal import Decimal

from django import forms
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory

from website.models import Order, OrderItem


order_number_validator = RegexValidator(
    regex=r'^[A-Za-z0-9-]+$',
    message='El número de pedido solo puede contener letras, números y guion.',
)

product_name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s.,-]+$',
    message='El producto contiene caracteres no permitidos.',
)


class OrderForm(forms.ModelForm):
    """
    Formulario principal para crear o actualizar un pedido.

    Convención Django: ModelForm.
    No es un patrón GoF del catálogo, pero Django lo usa para crear formularios
    desde modelos y concentrar validación de entrada.

    Este formulario trabaja con el modelo Order.
    Aquí se editan los datos generales del pedido, como:
    - número de pedido
    - estado del pedido
    - estado del pago

    El total no se edita manualmente: se calcula desde los items del pedido.
    """

    class Meta:
        # Modelo conectado a este formulario.
        model = Order

        # Campos del modelo Order que se mostrarán en el formulario HTML.
        fields = (
            'order_number',
            'status',
            'payment_status',
        )

        # Etiquetas visibles para cada campo.
        labels = {
            'order_number': 'Número de pedido',
            'status': 'Estado',
            'payment_status': 'Estado de pago',
        }

        # Widgets controlan cómo se renderiza cada input en HTML.
        # Aquí se agregan clases de Bootstrap para mantener el diseño.
        widgets = {
            'order_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ORD-001',
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'payment_status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }

        # Mensajes de validación del pedido en español.
        error_messages = {
            'order_number': {
                'required': 'Debes ingresar el número de pedido.',
                'unique': 'Ya existe un pedido con ese número.',
                'max_length': 'El número de pedido no puede superar 20 caracteres.',
            },
            'status': {
                'required': 'Debes seleccionar el estado del pedido.',
                'invalid_choice': 'Selecciona un estado de pedido válido.',
            },
            'payment_status': {
                'required': 'Debes seleccionar el estado de pago.',
                'invalid_choice': 'Selecciona un estado de pago válido.',
            },
        }

    def __init__(self, *args, **kwargs):
        """Agrega validación regex al número de pedido sin duplicarla en la vista."""
        super().__init__(*args, **kwargs)
        self.fields['order_number'].validators.append(order_number_validator)

    def clean_order_number(self):
        """
        Valida que el número público del pedido sea único con un mensaje en español.
        """
        order_number = self.cleaned_data.get('order_number', '').strip()

        if not order_number:
            return order_number

        existing_orders = Order.objects.filter(order_number__iexact=order_number)

        if self.instance.pk:
            existing_orders = existing_orders.exclude(pk=self.instance.pk)

        if existing_orders.exists():
            raise forms.ValidationError('Ya existe un pedido con ese número.')

        return order_number

class OrderItemForm(forms.ModelForm):
    """
    Formulario para cada item/producto dentro de un pedido.

    Convención Django: ModelForm especializado.
    Permite validar cada producto antes de convertirlo en OrderItem.

    Este formulario trabaja con el modelo OrderItem.
    Se usa dentro de un formset porque un pedido puede tener varios items.
    """

    def __init__(self, *args, **kwargs):
        """
        Personaliza el comportamiento inicial del formulario.

        La idea es permitir que aparezcan filas vacías en el formset
        sin que Django las marque inmediatamente como error.
        """
        super().__init__(*args, **kwargs)

        # Estos campos se marcan como no obligatorios inicialmente.
        # Luego en clean() validamos si el usuario empezó a llenar la fila.
        for field_name in ('product_name', 'quantity', 'unit_price'):
            self.fields[field_name].required = False

        # Seguridad de entrada: el producto acepta solo caracteres esperados.
        self.fields['product_name'].validators.append(product_name_validator)

        # Si el item todavía no existe en base de datos,
        # evitamos que cantidad y precio aparezcan con valores por defecto.
        if not self.instance.pk:
            self.fields['quantity'].initial = None
            self.fields['unit_price'].initial = None

    class Meta:
        # Modelo conectado a este formulario.
        model = OrderItem

        # Campos editables del item.
        fields = (
            'product_name',
            'quantity',
            'unit_price',
        )

        # Etiquetas visibles.
        labels = {
            'product_name': 'Producto',
            'quantity': 'Cantidad',
            'unit_price': 'Precio unitario',
        }

        # Apariencia HTML de los campos.
        widgets = {
            'product_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Producto',
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                }
            ),
            'unit_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                }
            ),
        }

        # Mensajes de validación de productos en español.
        error_messages = {
            'product_name': {
                'max_length': 'El producto no puede superar 100 caracteres.',
            },
            'quantity': {
                'invalid': 'Ingresa una cantidad válida.',
            },
            'unit_price': {
                'invalid': 'Ingresa un precio unitario válido.',
                'max_digits': 'El precio unitario no puede superar 10 dígitos.',
                'max_decimal_places': 'El precio unitario solo puede tener 2 decimales.',
            },
        }

    def clean_quantity(self):
        """
        Valida la cantidad del producto.

        Si la fila está vacía, se permite.
        Pero si el usuario escribe una cantidad, debe ser mayor a cero.
        """
        quantity = self.cleaned_data.get('quantity')

        if quantity in (None, ''):
            return quantity

        if quantity <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero.')

        return quantity

    def clean_unit_price(self):
        """
        Valida el precio unitario.

        Si la fila está vacía, se permite.
        Pero si el usuario escribe un precio, no puede ser negativo.
        """
        unit_price = self.cleaned_data.get('unit_price')

        if unit_price in (None, ''):
            return unit_price

        if unit_price < Decimal('0.00'):
            raise forms.ValidationError('El precio unitario no puede ser negativo.')

        return unit_price

    def clean(self):
        """
        Validación general del item.

        Esta función revisa la fila completa:
        - Si está vacía, la deja pasar.
        - Si el usuario llenó algo, exige que complete producto, cantidad y precio.
        - Si la fila está marcada para eliminar, no valida los campos.
        """
        cleaned_data = super().clean()

        # Si el usuario marcó este item para eliminar,
        # no tiene sentido validar sus campos.
        if cleaned_data.get('DELETE'):
            return cleaned_data

        product_name = cleaned_data.get('product_name')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')

        # Detecta si el usuario escribió algo en la fila.
        # Esto permite filas extra vacías sin obligar al usuario a completarlas.
        has_any_value = any(
            value not in (None, '')
            for value in (product_name, quantity, unit_price)
        )

        # Si la fila está completamente vacía, no se considera error.
        if not has_any_value:
            return cleaned_data

        # Si empezó a llenar la fila, entonces todos los campos son obligatorios.
        if not product_name:
            self.add_error('product_name', 'El producto es obligatorio.')

        if quantity in (None, ''):
            self.add_error('quantity', 'La cantidad es obligatoria.')

        if unit_price in (None, ''):
            self.add_error('unit_price', 'El precio unitario es obligatorio.')

        return cleaned_data


# Convención Django: FormSet.
# No pertenece al catálogo GoF; agrupa formularios hijos para una relación uno-a-muchos.
# FormSet para manejar varios OrderItem dentro de un mismo Order.
#
# Esto permite que en una sola pantalla puedas:
# - crear un pedido
# - agregar varios productos
# - editar productos existentes
# - eliminar productos del pedido
OrderItemFormSet = inlineformset_factory(
    Order,              # Modelo padre.
    OrderItem,          # Modelo hijo.
    form=OrderItemForm, # Formulario que usará cada item.
    extra=1,            # Cantidad de filas vacías adicionales.
    can_delete=True,    # Permite eliminar items existentes.
)
