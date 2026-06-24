# Tests de Django

from django.conf import settings # Importa las variables de entorno del proyecto.
from django.contrib.auth import get_user_model # Importa el modelo de usuario.
from django.contrib.messages import get_messages
from django.test import Client, TestCase # Importa las clases de pruebas.
from django.urls import reverse # Importa las funciones de URL.

from website.forms import OrderForm, OrderItemForm, SignUpForm
from website.models import Order, OrderItem


class HomeViewTests(TestCase): #
    """Verifica el formulario visible en la página principal."""

    def test_login_form_posts_to_login_route(self): # funcion de prueba
        # home redirige a login; allí se protege que el formulario envíe a la ruta correcta.
        response = self.client.get(reverse('login')) # lo que hace es obtener la URL del formulario.
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

    def test_invalid_csrf_post_redirects_to_login(self):
        # Simula el caso del navegador enviando un formulario sin token válido.
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            reverse('login'),
            {'username': 'Braianprueba', 'password': 'prueba1234'},
        )

        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)


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

    def test_order_form_uses_buttons_for_product_rows(self):
        # La interfaz de productos usa botones Bootstrap y mantiene DELETE oculto para Django.
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('create_order'))

        self.assertContains(response, 'id="addOrderItem"')
        self.assertContains(response, 'Agregar producto')
        self.assertContains(response, 'order-remove-item')
        self.assertContains(response, 'Quitar')
        self.assertNotContains(response, 'Marcar')


class LoginValidationTests(TestCase):
    """Verifica mensajes de inicio de sesión en español."""

    def test_empty_login_uses_spanish_validation_message(self):
        # Valida que el login manual no muestre mensajes genéricos en inglés.
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        messages = [str(message) for message in get_messages(response.wsgi_request)]

        self.assertRedirects(response, reverse('login'))
        self.assertIn('Debes ingresar usuario y contraseña.', messages)


class SignUpFormValidationTests(TestCase):
    """Verifica mensajes de registro en español."""

    def test_required_registration_fields_use_labels_and_spanish_messages(self):
        # Los labels evitan que el template muestre errores con prefijo vacío, como ": required".
        form = SignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.fields['username'].label, 'Usuario')
        self.assertIn('Debes ingresar un nombre de usuario.', form.errors['username'])
        self.assertIn('Debes ingresar tu nombre.', form.errors['first_name'])
        self.assertIn('Debes ingresar tu apellido.', form.errors['last_name'])
        self.assertIn('Debes ingresar un correo electrónico.', form.errors['email'])
        self.assertIn('Debes ingresar una contraseña.', form.errors['password1'])
        self.assertIn('Debes confirmar la contraseña.', form.errors['password2'])

    def test_password_mismatch_uses_spanish_message(self):
        form = SignUpForm(
            data={
                'username': 'cliente1',
                'first_name': 'Cliente',
                'last_name': 'Prueba',
                'email': 'cliente@example.com',
                'password1': 'clave-segura-123',
                'password2': 'otra-clave-123',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Las contraseñas no coinciden.', form.errors['password2'])


class OrderFormValidationTests(TestCase):
    """Verifica mensajes de pedidos en español."""

    def test_required_order_fields_use_spanish_messages(self):
        # El formulario padre traduce los errores obligatorios del ModelForm.
        form = OrderForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('Debes ingresar el número de pedido.', form.errors['order_number'])
        self.assertNotIn('total', form.fields)
        self.assertNotIn('total', form.errors)

    def test_duplicate_order_number_uses_spanish_message(self):
        Order.objects.create(order_number='ORD-001', total='10.00')

        form = OrderForm(
            data={
                'order_number': 'ord-001',
                'status': Order.STATUS_PENDING,
                'payment_status': Order.PAYMENT_PENDING,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Ya existe un pedido con ese número.', form.errors['order_number'])

    def test_started_order_item_requires_complete_row_in_spanish(self):
        # Si el usuario empieza una fila de producto, se exige completarla en español.
        form = OrderItemForm(data={'product_name': 'Teclado', 'quantity': '', 'unit_price': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('La cantidad es obligatoria.', form.errors['quantity'])
        self.assertIn('El precio unitario es obligatorio.', form.errors['unit_price'])

    def test_order_total_is_calculated_from_items(self):
        order = Order.objects.create(order_number='ORD-002')
        OrderItem.objects.create(
            order=order,
            product_name='Camisa',
            quantity=10,
            unit_price='1000.00',
        )
        OrderItem.objects.create(
            order=order,
            product_name='Pantalón',
            quantity=2,
            unit_price='5000.00',
        )

        total = order.calculate_total()
        order.refresh_from_db()

        self.assertEqual(total, order.total)
        self.assertEqual(order.total, 20000)

    def test_order_total_becomes_zero_without_items(self):
        order = Order.objects.create(order_number='ORD-003', total='999.00')

        total = order.calculate_total()
        order.refresh_from_db()

        self.assertEqual(total, 0)
        self.assertEqual(order.total, 0)

    def test_create_order_calculates_total_from_posted_items(self):
        admin_user = get_user_model().objects.create_user(
            username='AdminCreatesOrder',
            password='admin1234',
            is_staff=True,
        )
        self.client.force_login(admin_user)

        response = self.client.post(
            reverse('create_order'),
            {
                'order_number': 'ORD-POST',
                'status': Order.STATUS_PENDING,
                'payment_status': Order.PAYMENT_PENDING,
                'items-TOTAL_FORMS': '2',
                'items-INITIAL_FORMS': '0',
                'items-MIN_NUM_FORMS': '0',
                'items-MAX_NUM_FORMS': '1000',
                'items-0-product_name': 'Camisa',
                'items-0-quantity': '3',
                'items-0-unit_price': '1000.00',
                'items-1-product_name': 'Pantalón',
                'items-1-quantity': '2',
                'items-1-unit_price': '5000.00',
            },
        )
        order = Order.objects.get(order_number='ORD-POST')

        self.assertRedirects(response, reverse('orders'))
        self.assertEqual(order.total, 13000)
