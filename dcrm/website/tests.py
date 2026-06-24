# Tests de Django

from django.conf import settings # Importa las variables de entorno del proyecto.
from django.contrib.auth import get_user_model # Importa el modelo de usuario.
from django.test import Client, TestCase # Importa las clases de pruebas.
from django.urls import reverse # Importa las funciones de URL.


class HomeViewTests(TestCase): #
    """Verifica el formulario visible en la página principal."""

    def test_login_form_posts_to_login_route(self): # funcion de prueba
        # Protege el bug donde el formulario enviaba a `home` en vez de `login`.
        response = self.client.get(reverse('home')) # lo que hace es obtener la URL del formulario.
        # Verifica que el formulario se envía a la ruta correcta

        self.assertContains(response, f'action="{reverse("login")}"')


class SecuritySettingsTests(TestCase): # esta clase se ejecuta antes de las pruebas
    """Protege la configuración necesaria para desarrollo local."""

    def test_debug_mode_does_not_force_secure_cookies(self): # Funcion de prueba para el login
        # En desarrollo local se usa HTTP, por eso estas cookies no deben exigir HTTPS.
        # Si estas cookies se marcan como seguras en HTTP local, el login no persiste.
        self.assertFalse(settings.SESSION_COOKIE_SECURE)
        self.assertFalse(settings.CSRF_COOKIE_SECURE)

    def test_project_uses_custom_csrf_failure_view(self):
        # El error CSRF debe volver a la app con mensaje claro, no mostrar el 403 técnico.
        self.assertEqual(settings.CSRF_FAILURE_VIEW, 'website.views.csrf_failure')


class LoginFlowTests(TestCase): # Esta clase se ejecuta antes de las pruebas
    """Comprueba que el flujo de autenticación conserva la sesión."""

    def setUp(self): # es para crear un usuario
        # Usuario mínimo para probar el flujo completo de login.
        self.user = get_user_model().objects.create_user(
            username='Braianprueba',
            password='prueba1234',
        ) # usando el modelo de usuario y la contraseña.

    def test_login_view_authenticates_and_saves_session(self): #esta funcion para el login
        # El usuario se autentica y se guarda la sesión.
        response = self.client.post(
            reverse('login'),
            {'username': 'Braianprueba', 'password': 'prueba1234'},
        ) # se crea un cliente para el login y se envia la url de login con los datos del usuario

        self.assertRedirects(response, reverse('home')) # Se comprueba que se redirija a la página principal.
        self.assertEqual(str(self.user.pk), self.client.session.get('_auth_user_id')) # y se comprueba que el ID del usuario esté en la sesión.

    def test_admin_login_redirects_to_orders(self):
        # Admin se define como usuario staff o superusuario según la regla del proyecto.
        admin_user = get_user_model().objects.create_user(
            username='Adminprueba',
            password='admin1234',
            is_staff=True,
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'Adminprueba', 'password': 'admin1234'},
        )

        self.assertRedirects(response, reverse('orders'))
        self.assertEqual(str(admin_user.pk), self.client.session.get('_auth_user_id'))

    def test_invalid_csrf_post_redirects_to_home(self):
        # Simula el caso del navegador enviando un formulario sin token válido.
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            reverse('login'),
            {'username': 'Braianprueba', 'password': 'prueba1234'},
        )

        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)


class OrderRoleAccessTests(TestCase):
    """Verifica que solo Admin pueda administrar pedidos."""

    def setUp(self):
        self.client_user = get_user_model().objects.create_user(
            username='Clienteprueba',
            password='cliente1234',
        )
        self.admin_user = get_user_model().objects.create_user(
            username='Adminorders',
            password='admin1234',
            is_staff=True,
        )

    def test_client_cannot_access_orders_module(self):
        # Patrón GoF Decorator: user_passes_test bloquea clientes autenticados.
        self.client.force_login(self.client_user)

        response = self.client.get(reverse('orders'))

        self.assertRedirects(
            response,
            f'{reverse("home")}?next={reverse("orders")}',
        )

    def test_admin_can_access_orders_module(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('orders'))

        self.assertEqual(response.status_code, 200)
