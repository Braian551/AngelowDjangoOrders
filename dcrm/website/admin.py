#admin en donde se registra el modelo.
from django.contrib import admin

from .models import ( # Importa los modelos para administrarlos en el
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
admin.site.register(Record)# Registra el modelo Record para administrarlo desde el panel de Django.
admin.site.register(Order) # Registra el modelo Order para administrarlo desde el
admin.site.register(OrderItem) # Registro del modelo OrderItem
admin.site.register(OrderStatusHistory) # Registro del modelo OrderStatusHistory
admin.site.register(StockReservation) # Registro del modelo StockReservation
admin.site.register(OrderView) # Registro del modelo OrderView
