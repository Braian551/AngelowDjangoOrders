from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from website.forms import OrderForm, OrderItemFormSet
from website.models import Order, OrderView, StockReservation


def sync_stock_reservations(order):
    """Sincroniza las reservas de stock según los items actuales del pedido."""
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
    username = user.get_username() if user.is_authenticated else ''
    OrderView.objects.create(order=order, viewed_by=username)


@login_required(login_url='home')
def list_orders(request):
    """Muestra el listado de pedidos."""
    orders = Order.objects.prefetch_related('items').all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='home')
def create_order(request):
    """Crea un pedido junto con sus items."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save()

            formset.instance = order
            formset.save()

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


@login_required(login_url='home')
def update_order(request, order_id):
    """Actualiza un pedido existente y sus items."""
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.save()

            sync_stock_reservations(order)

            if order.items.exists():
                order.calculate_total()

            messages.success(request, 'Pedido actualizado correctamente.')
            return redirect('orders')
    else:
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


@login_required(login_url='home')
def delete_order(request, order_id):
    """Elimina un pedido después de confirmarlo."""
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
        return redirect('orders')

    record_order_view(order, request.user)
    return render(request, 'orders/order_confirm_delete.html', {'order': order})