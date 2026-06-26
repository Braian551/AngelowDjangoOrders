"""Registro de modelos en el panel administrativo de Django."""

from django.contrib import admin

from .models import (
    Record,
    Order,
    OrderItem,
    OrderStatusHistory,
    StockReservation,
    OrderView,
)


# Convención Admin de Django:
# el framework genera CRUD administrativo a partir del registro de cada modelo.
# Cada registro habilita la gestión del modelo desde el panel `/admin/`.
admin.site.register(Record)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(StockReservation)
admin.site.register(OrderView)
