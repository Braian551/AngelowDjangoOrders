# Tests de Django 

from django.conf import settings # Importa las variables de entorno del proyecto.
from django.contrib.auth import get_user_model # Importa el modelo de usuario.
from django.test import TestCase # Importa las clases de pruebas.
from django.urls import reverse # Importa las funciones de URL.


class HomeViewTests(TestCase): # 
    """Verifica el formulario visible en la página principal."""

    def test_login_form_posts_to_login_route(self): # funcion de prueba
        response = self.client.get(reverse('home')) # lo que hace es obtener la URL del formulario.
        # Verifica que el formulario se envía a la ruta correcta

        self.assertContains(response, f'action="{reverse("login")}"')


class SecuritySettingsTests(TestCase): # esta clase se ejecuta antes de las pruebas 
    """Protege la configuración necesaria para desarrollo local."""

    def test_debug_mode_does_not_force_secure_cookies(self): # Funcion de prueba para el login
        # Si estas cookies se marcan como seguras en HTTP local, el login no persiste.
        self.assertFalse(settings.SESSION_COOKIE_SECURE)
        self.assertFalse(settings.CSRF_COOKIE_SECURE)


class LoginFlowTests(TestCase): # Esta clase se ejecuta antes de las pruebas
    """Comprueba que el flujo de autenticación conserva la sesión."""

    def setUp(self): # es para crear un usuario
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
