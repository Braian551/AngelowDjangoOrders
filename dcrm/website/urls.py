from django.urls import path

from . import views


# Convención Django de enrutamiento.
# No es un patrón GoF del catálogo; este archivo decide qué vista atiende cada URL.
# Rutas disponibles para la aplicación website.
# Mantener nombres estables evita romper los `{% url %}` usados por las plantillas.
urlpatterns = [
    # Página principal y autenticación.
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registrar/', views.register_user, name='register'),

    # Acciones sobre registros de clientes.
    path('record/<str:pk>/', views.customer_record, name='customer_record'),
    path('delete_record/<str:pk>/', views.delete_record, name='delete_record'),
    path('update_record/<str:pk>/', views.update_record, name='update_record'),

    # Acciones sobre pedidos.
    path('orders/', views.list_orders, name='orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/edit/', views.update_order, name='update_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
]
