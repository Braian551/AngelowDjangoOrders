from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie

from website.forms import SignUpForm
from .helpers import get_login_redirect_url, paginate_records


@never_cache
@ensure_csrf_cookie
def home(request):
    """Renderiza la página principal con registros paginados."""
    # La misma vista muestra login o dashboard según el estado de autenticación.
    # ensure_csrf_cookie entrega un token fresco para el formulario de inicio de sesión.
    records = paginate_records(request)
    return render(request, 'home.html', {'records': records})


@never_cache
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
            # La redirección depende del rol: Admin va a pedidos y Cliente al inicio.
            return redirect(get_login_redirect_url(user))

        messages.error(request, "las credenciales son inválidas")
        return redirect('home')

    return redirect('home')

# never cache es para que no se cachee la página de inicio.
@never_cache
def logout_user(request):
    """Cierra la sesión actual y vuelve a la página principal."""
    logout(request)
    messages.success(request, "cerraste la sesión correctamente")
    return redirect('home')


@never_cache
@ensure_csrf_cookie #ensure csrf cookie es para que Django genere el cookie csrf_token.

def register_user(request):
    """Registra un usuario nuevo y lo autentica automáticamente."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # Después del registro se inicia sesión para evitar pedir login otra vez.
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "registro exitoso")
            # Los usuarios registrados quedan como Cliente salvo que se les active is_staff.
            return redirect(get_login_redirect_url(user))
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def csrf_failure(request, reason=''):
    """Redirige los fallos CSRF a un mensaje entendible para el usuario."""
    # Django rota el token al iniciar sesión; si se reenvía un formulario viejo aparece 403.
    messages.error(
        request,
        "El formulario expiró o pertenece a una sesión anterior. Recarga la página e inténtalo de nuevo.",
    )
    return redirect('home')
