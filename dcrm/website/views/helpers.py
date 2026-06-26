from django.core.paginator import Paginator

from website.models import Record


# Patrón GoF de comportamiento: Strategy.
# Estas funciones encapsulan reglas de rol y redirección para que las vistas
# no repitan condiciones como `is_staff or is_superuser`.
def is_admin_user(user):
    """
    Verifica si el usuario tiene rol de administrador.

    Reglas del proyecto:
    - Admin: superusuario o usuario con is_staff=True.
    - Cliente: usuario autenticado normal, sin permisos administrativos.
    """
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def get_login_redirect_url(user):
    """
    Devuelve la ruta a la que debe ir el usuario después de iniciar sesión.

    Esta función centraliza la política de roles para no duplicarla en las vistas.

    Reglas:
    - Admin: entra al módulo de pedidos.
    - Cliente: vuelve al inicio.
    """
    if is_admin_user(user):
        return 'orders'

    return 'home'


def paginate_records(request):
    """
    Devuelve los registros de clientes paginados para el dashboard.

    Se ordenan del más reciente al más antiguo para mostrar primero
    los registros nuevos.
    """
    # ORM / Active Record: Django traduce esta consulta a SQL sin escribirlo a mano.
    records_list = Record.objects.all().order_by('-created_at')

    # Ocho registros por página mantiene la tabla legible.
    paginator = Paginator(records_list, 8)

    page_number = request.GET.get('page')

    return paginator.get_page(page_number)
