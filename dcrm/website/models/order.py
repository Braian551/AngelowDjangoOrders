from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Order(models.Model):
    """Modelo para representar un pedido dentro del sistema."""

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_PROCESSING, 'En proceso'),
        (STATUS_COMPLETED, 'Completado'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]

    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_FAILED = 'failed'
    PAYMENT_REFUNDED = 'refunded'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pendiente'),
        (PAYMENT_PAID, 'Pagado'),
        (PAYMENT_FAILED, 'Fallido'),
        (PAYMENT_REFUNDED, 'Reembolsado'),
    ]

    # Número público del pedido; debe ser único para poder buscarlo y auditarlo.
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_PENDING,
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        """Devuelve el número de pedido como representación legible."""
        return self.order_number

    def calculate_total(self):
        """Calcula el total sumando los subtotales de los ítems asociados."""
        if not self.pk or not self.items.exists():
            return self.total

        total = sum((item.subtotal for item in self.items.all()), Decimal('0.00'))
        self.total = total
        self.save(update_fields=['total', 'updated_at'])
        return total

    def change_status(self, new_status, new_payment_status=None, note=''):
        """Cambia el estado del pedido y registra el movimiento en el historial."""
        valid_statuses = dict(self.STATUS_CHOICES)
        valid_payment_statuses = dict(self.PAYMENT_STATUS_CHOICES)

        if new_status not in valid_statuses:
            raise ValidationError('El estado del pedido no es válido.')

        if new_payment_status and new_payment_status not in valid_payment_statuses:
            raise ValidationError('El estado de pago no es válido.')

        previous_status = self.status
        previous_payment_status = self.payment_status
        update_fields = []

        if self.status != new_status:
            self.status = new_status
            update_fields.append('status')

        if new_payment_status and self.payment_status != new_payment_status:
            self.payment_status = new_payment_status
            update_fields.append('payment_status')

        if update_fields:
            self.save(update_fields=update_fields + ['updated_at'])

            # Guardar el historial permite auditar cada transición importante del pedido.
            OrderStatusHistory.objects.create(
                order=self,
                previous_status=previous_status,
                new_status=self.status,
                previous_payment_status=previous_payment_status,
                new_payment_status=self.payment_status,
                note=note,
            )

        return self


class OrderItem(models.Model):
    """Modelo para representar un producto dentro de un pedido."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Ítem de pedido'
        verbose_name_plural = 'Ítems de pedido'

    def __str__(self):
        """Muestra el nombre del producto y la cantidad solicitada."""
        return f'{self.product_name} x{self.quantity}'

    @property
    def subtotal(self):
        """Calcula el subtotal del ítem usando cantidad por precio unitario."""
        return self.quantity * self.unit_price


class OrderStatusHistory(models.Model):
    """Modelo para registrar cada cambio de estado de un pedido."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, blank=True)
    new_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    previous_payment_status = models.CharField(
        max_length=20,
        choices=Order.PAYMENT_STATUS_CHOICES,
        blank=True,
    )
    new_payment_status = models.CharField(max_length=20, choices=Order.PAYMENT_STATUS_CHOICES)
    note = models.CharField(max_length=255, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Historial de estado'
        verbose_name_plural = 'Historial de estados'

    def __str__(self):
        """Muestra la transición de estado asociada al pedido."""
        return f'{self.order.order_number}: {self.previous_status} -> {self.new_status}'


class StockReservation(models.Model):
    """Modelo para representar una reserva de stock asociada a un ítem."""

    STATUS_RESERVED = 'reserved'
    STATUS_EXPIRED = 'expired'
    STATUS_RELEASED = 'released'
    STATUS_CHOICES = [
        (STATUS_RESERVED, 'Reservado'),
        (STATUS_EXPIRED, 'Expirado'),
        (STATUS_RELEASED, 'Liberado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='stock_reservations')
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='stock_reservation',
    )
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_RESERVED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reserva de stock'
        verbose_name_plural = 'Reservas de stock'

    def __str__(self):
        """Muestra el producto reservado y el estado legible de la reserva."""
        return f'{self.product_name} - {self.get_status_display()}'

    def reserve(self):
        """Establece la reserva como activa."""
        self.status = self.STATUS_RESERVED
        self.save(update_fields=['status', 'updated_at'])
        return self

    def expire(self):
        """Marca la reserva como expirada."""
        self.status = self.STATUS_EXPIRED
        self.save(update_fields=['status', 'updated_at'])
        return self

    def release(self):
        """Libera la reserva de stock."""
        self.status = self.STATUS_RELEASED
        self.save(update_fields=['status', 'updated_at'])
        return self


class OrderView(models.Model):
    """Modelo para registrar cuándo y por quién fue visto un pedido."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='view_logs')
    viewed_by = models.CharField(max_length=150, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = 'Vista de pedido'
        verbose_name_plural = 'Vistas de pedidos'

    def __str__(self):
        """Muestra el número de pedido y el usuario que lo visualizó."""
        return f'{self.order.order_number} visto por {self.viewed_by or "anónimo"}'
