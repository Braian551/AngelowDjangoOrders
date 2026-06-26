"""Exporta las vistas públicas que usa `website.urls`.

Arquitectura Django MTV:
las vistas coordinan request, formularios, modelos, mensajes y templates.
"""

from .auth_views import csrf_failure, home, login_user, logout_user, register_user
from .record_views import customer_record, delete_record, update_record
from .order_views import (
    list_orders,
    create_order,
    update_order,
    delete_order,
)
