from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from website.models import Order, OrderStatusHistory


# Patrón GoF de comportamiento: Observer.
# Django dispara señales y estas funciones reaccionan sin acoplarse a cada vista.
# Estas señales mantienen el historial aunque el pedido se guarde desde admin,
# vistas, shell o cualquier otro punto del proyecto.
@receiver(pre_save, sender=Order)
def capture_previous_order_state(sender, instance, **kwargs):
    """
    Captura el estado anterior de un pedido antes de guardarlo.

    Esto se usa para comparar después si el estado del pedido
    o el estado del pago cambiaron.
    """

    # Si el pedido todavía no existe en base de datos,
    # significa que se está creando por primera vez.
    if not instance.pk:
        instance._previous_status = ''
        instance._previous_payment_status = ''
        return

    # Busca el pedido actual en la base de datos antes de guardar los nuevos cambios.
    previous_order = sender.objects.filter(pk=instance.pk).only(
        'status',
        'payment_status',
    ).first()

    # Si no se encuentra el pedido anterior, se dejan valores vacíos.
    if previous_order is None:
        instance._previous_status = ''
        instance._previous_payment_status = ''
        return

    # Guarda temporalmente los valores anteriores dentro del objeto.
    # Estos atributos no son campos de base de datos.
    instance._previous_status = previous_order.status
    instance._previous_payment_status = previous_order.payment_status


@receiver(post_save, sender=Order)
def create_order_status_history(sender, instance, created, **kwargs):
    """
    Crea un registro histórico cuando se crea un pedido
    o cuando cambia su estado o estado de pago.
    """

    # Recupera los valores anteriores capturados en pre_save.
    previous_status = getattr(instance, '_previous_status', '')
    previous_payment_status = getattr(instance, '_previous_payment_status', '')

    # Si el pedido fue creado por primera vez, se registra el historial inicial.
    if created:
        OrderStatusHistory.objects.create(
            order=instance,
            previous_status='',
            new_status=instance.status,
            previous_payment_status='',
            new_payment_status=instance.payment_status,
            note='Pedido creado',
        )
        return

    # Si el pedido ya existía, solo se crea historial cuando cambia
    # el estado del pedido o el estado de pago.
    if (
        previous_status != instance.status
        or previous_payment_status != instance.payment_status
    ):
        OrderStatusHistory.objects.create(
            order=instance,
            previous_status=previous_status,
            new_status=instance.status,
            previous_payment_status=previous_payment_status,
            new_payment_status=instance.payment_status,
            note='Pedido actualizado',
        )
