from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from website.forms import SignUpForm
from .helpers import paginate_records


def home(request):
    records = paginate_records(request)
    return render(request, 'home.html', {'records': records})


def login_user(request):
    """Procesa el inicio de sesión del usuario."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validar datos mínimos evita autenticar envíos vacíos o incompletos.
        if not username or not password:
            messages.error(request, "debes ingresar usuario y contraseña")
            return redirect('home')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Crear la sesión aquí permite que Django recuerde al usuario entre requests.
            login(request, user)
            messages.success(request, "ingresado exitosamente")
            return redirect('home')

        messages.error(request, "las credenciales son inválidas")
        return redirect('home')

    return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, "cerraste la sesión correctamente")
    return redirect('home')


def register_user(request):
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
