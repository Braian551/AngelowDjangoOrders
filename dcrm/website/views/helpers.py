#Este view para logica adicional
from django.core.paginator import Paginator

from website.models import Record


def paginate_records(request):
    """Devuelve los registros de clientes paginados para la página principal."""
    records_list = Record.objects.all().order_by('-created_at')
    paginator = Paginator(records_list, 8)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)