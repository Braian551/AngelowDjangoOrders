from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from website.forms import OrderForm, OrderItemFormSet
from website.models import Order, OrderView, StockReservation
from .helpers import is_admin_user


# Arquitectura Django MTV:
# las vistas coordinan modelos, formularios y plantillas sin guardar HTML ni SQL directo.
def sync_stock_reservations(order):
    """Sincroniza las reservas de stock según los items actuales del pedido."""
    # Cada ítem debe tener una reserva asociada para mantener trazabilidad del stock.
    for item in order.items.all():
        StockReservation.objects.update_or_create(
            order_item=item,
            defaults={
                'order': order,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'status': StockReservation.STATUS_RESERVED,
            },
        )


def record_order_view(order, user):
    """Registra quién visualizó un pedido."""
    # Guardar el nombre como texto evita depender de una relación directa con User.
    username = user.get_username() if user.is_authenticated else ''
    OrderView.objects.create(order=order, viewed_by=username)


# Patrón GoF estructural: Decorator.
# login_required valida sesión y user_passes_test agrega la autorización de rol Admin.
@login_required(login_url='home')
@user_passes_test(is_admin_user, login_url='home')
def list_orders(request):
    """Muestra el listado de pedidos."""
    # prefetch_related evita consultas repetidas al mostrar los items de cada pedido.
    orders = Order.objects.prefetch_related('items').all()
    return render(request, 'orders/order_list.html', {'orders': orders})


# Patrón GoF estructural: Decorator aplicado a la creación de pedidos.
@login_required(login_url='home')
@user_passes_test(is_admin_user, login_url='home')
def create_order(request):
    """Crea un pedido junto con sus items."""
    # Patrón web Post/Redirect/Get: si el POST es válido, se redirige para evitar reenvíos.
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            # Primero se guarda el pedido padre para que el formset pueda asociar sus items.
            order = form.save()

            formset.instance = order
            formset.save()

            # Las reservas dependen de los items finales guardados en la base de datos.
            sync_stock_reservations(order)

            if order.items.exists():
                order.calculate_total()

            messages.success(request, 'Pedido creado correctamente.')
            return redirect('orders')
    else:
        form = OrderForm()
        formset = OrderItemFormSet(prefix='items')

    context = {
        'form': form,
        'formset': formset,
        'page_title': 'Crear pedido',
        'submit_label': 'Guardar pedido',
    }

    return render(request, 'orders/order_form.html', context)


# Patrón GoF estructural: Decorator aplicado a la edición de pedidos.
@login_required(login_url='home')
@user_passes_test(is_admin_user, login_url='home')
def update_order(request, order_id):
    """Actualiza un pedido existente y sus items."""
    # La vista actúa como coordinadora: carga modelo, valida formularios y renderiza template.
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.save()

            # Después de editar items se actualizan reservas y total del pedido.
            sync_stock_reservations(order)

            if order.items.exists():
                order.calculate_total()

            messages.success(request, 'Pedido actualizado correctamente.')
            return redirect('orders')
    else:
        # Las visualizaciones se registran solo al abrir el pedido, no al enviar cambios.
        record_order_view(order, request.user)
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order, prefix='items')

    context = {
        'form': form,
        'formset': formset,
        'order': order,
        'page_title': 'Editar pedido',
        'submit_label': 'Actualizar pedido',
    }

    return render(request, 'orders/order_form.html', context)


# Patrón GoF estructural: Decorator aplicado a la eliminación de pedidos.
@login_required(login_url='home')
@user_passes_test(is_admin_user, login_url='home')
def delete_order(request, order_id):
    """Elimina un pedido después de confirmarlo."""
    # Separar GET de POST aplica confirmación explícita antes de ejecutar una acción destructiva.
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        # La eliminación real ocurre únicamente después de confirmar por POST.
        order.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
        return redirect('orders')

    record_order_view(order, request.user)
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
