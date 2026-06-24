from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie

from website.forms import SignUpForm
from .helpers import get_login_redirect_url, paginate_records


@never_cache
def home(request):
    """
    Renderiza el dashboard principal.

    Esta vista ya no mezcla login y dashboard.
    Si el usuario no ha iniciado sesión, se redirige a la vista de login.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    # Se obtienen los registros paginados para mostrarlos en la tabla principal.
    records = paginate_records(request)

    return render(request, 'home.html', {'records': records})


@never_cache
@ensure_csrf_cookie
def login_user(request):
    """
    Muestra y procesa el inicio de sesión.

    GET:
    - Muestra el formulario de login.

    POST:
    - Recibe usuario y contraseña.
    - Autentica al usuario.
    - Crea sesión si las credenciales son correctas.
    - Redirige según el rol del usuario.
    """
    if request.user.is_authenticated:
        return redirect(get_login_redirect_url(request.user))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validar datos mínimos evita autenticar formularios vacíos.
        if not username or not password:
            messages.error(request, 'Debes ingresar usuario y contraseña.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Crea la sesión del usuario en Django.
            login(request, user)

            messages.success(request, 'Ingresaste exitosamente.')

            # Redirección por rol:
            # Admin va a orders.
            # Cliente va a home.
            return redirect(get_login_redirect_url(user))

        messages.error(request, 'Las credenciales son inválidas.')
        return redirect('login')

    return render(request, 'login.html')


@never_cache
def logout_user(request):
    """
    Cierra la sesión actual y vuelve a la pantalla de login.

    never_cache evita que el navegador muestre una pantalla anterior
    después de cerrar sesión usando el botón de volver.
    """
    logout(request)
    messages.success(request, 'Cerraste la sesión correctamente.')
    return redirect('login')


@never_cache
@ensure_csrf_cookie
def register_user(request):
    """
    Registra un usuario nuevo y lo autentica automáticamente.

    Los usuarios registrados quedan como Cliente por defecto.
    Para que sean Admin, se les debe activar is_staff o is_superuser.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Registro exitoso.')
            return redirect(get_login_redirect_url(user))
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def csrf_failure(request, reason=''):
    """
    Maneja errores CSRF de forma entendible para el usuario.

    Este error puede ocurrir cuando:
    - El formulario expiró.
    - El usuario inició/cerró sesión en otra pestaña.
    - Se reenvió un formulario viejo.
    """
    messages.error(
        request,
        'El formulario expiró o pertenece a una sesión anterior. Recarga la página e inténtalo de nuevo.',
    )

    return redirect('login')