#Crud de records
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from website.forms import RecordForm
from website.models import Record


def customer_record(request, pk):
    """Muestra el detalle de un cliente solo si el usuario inició sesión."""
    if request.user.is_authenticated:
        customer_record = get_object_or_404(Record, id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})

    messages.error(request, "debes iniciar sesión para ver el registro del cliente")
    return redirect('home')


def delete_record(request, pk):
    """Elimina un registro de cliente cuando el usuario está autenticado."""
    if request.user.is_authenticated:
        delete_it = get_object_or_404(Record, id=pk)
        delete_it.delete()
        messages.success(request, "registro eliminado correctamente")
        return redirect('home')

    messages.error(request, "debes iniciar sesión para eliminar el registro del cliente")
    return redirect('home')


def update_record(request, pk):
    """Actualiza los datos de un cliente existente."""
    if request.user.is_authenticated:
        current_record = get_object_or_404(Record, id=pk)
        form = RecordForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "registro actualizado correctamente")
            return redirect('home')

        return render(request, 'update_record.html', {'form': form})

    messages.error(request, "debes iniciar sesión para actualizar el registro del cliente")
    return redirect('home')