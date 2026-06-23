from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import RecordForm, SignUpForm
from .models import Record


# Consulta base de registros. Se conserva para mantener la estructura original del proyecto.
records = Record.objects.all()


def paginate_records(request):
    """Devuelve los registros de clientes paginados para la página principal."""
    records_list = Record.objects.all().order_by('-created_at')
    paginator = Paginator(records_list, 8)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def home(request):
    """Muestra el inicio y procesa el formulario de inicio de sesión."""
    records = paginate_records(request)

    # Si llega un POST, se intenta autenticar al usuario con los datos enviados.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "ingresado exitosamente")
            return redirect('home')

        messages.error(request, "las credenciales son inválidas")
        return render(request, 'home.html', {'records': records})

    # Para peticiones GET solo se renderiza la página con la lista de registros.
    return render(request, 'home.html', {'records': records})


def login_user(request):
    """Vista reservada para iniciar sesión si se decide separar esta lógica."""
    pass


def logout_user(request):
    """Cierra la sesión del usuario actual y vuelve al inicio."""
    logout(request)
    messages.success(request, "cerraste la sesión correctamente")
    return redirect('home')


def register_user(request):
    """Crea un usuario nuevo y lo autentica automáticamente al registrarse."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "registro exitoso")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    """Muestra el detalle de un cliente solo si el usuario inició sesión."""
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})

    messages.error(request, "debes iniciar sesión para ver el registro del cliente")
    return redirect('home')


def delete_record(request, pk):
    """Elimina un registro de cliente cuando el usuario está autenticado."""
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "registro eliminado correctamente")
        return redirect('home')

    messages.error(request, "debes iniciar sesión para eliminar el registro del cliente")
    return redirect('home')


def update_record(request, pk):
    """Actualiza los datos de un cliente existente."""
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = RecordForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "registro actualizado correctamente")
            return redirect('home')

        return render(request, 'update_record.html', {'form': form})

    messages.error(request, "debes iniciar sesión para actualizar el registro del cliente")
    return redirect('home')
