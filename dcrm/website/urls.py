from django.urls import path

from . import views


# Rutas disponibles para la aplicación website.
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
]
