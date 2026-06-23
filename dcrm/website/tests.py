from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    """Verifica el formulario visible en la página principal."""

    def test_login_form_posts_to_login_route(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, f'action="{reverse("login")}"')


class SecuritySettingsTests(TestCase):
    """Protege la configuración necesaria para desarrollo local."""

    def test_debug_mode_does_not_force_secure_cookies(self):
        # Si estas cookies se marcan como seguras en HTTP local, el login no persiste.
        self.assertFalse(settings.SESSION_COOKIE_SECURE)
        self.assertFalse(settings.CSRF_COOKIE_SECURE)


class LoginFlowTests(TestCase):
    """Comprueba que el flujo de autenticación conserva la sesión."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='angelo',
            password='ClaveSegura123',
        )

    def test_login_view_authenticates_and_saves_session(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'angelo', 'password': 'ClaveSegura123'},
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(str(self.user.pk), self.client.session.get('_auth_user_id'))
