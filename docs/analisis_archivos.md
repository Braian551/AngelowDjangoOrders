# Analisis archivo por archivo

Este resumen documenta la responsabilidad principal de cada archivo relevante del proyecto AngeloDjangoOrders.

## Raiz del proyecto

- `requirements.txt`: define Django, PyMySQL, cryptography, python-dotenv y sqlparse.
- `Dockerfile`: construye la imagen Python/Django, instala dependencias y expone el servidor en el puerto 8000.
- `docker-compose.yml`: levanta los servicios `web` y `db`, conecta Django con MySQL y define el volumen persistente.
- `.env.example`: documenta las variables de entorno esperadas para la base de datos.
- `docker/entrypoint.sh`: ejecuta migraciones y arranca `runserver`.

## Proyecto Django `dcrm/`

- `dcrm/manage.py`: punto de entrada para comandos Django.
- `dcrm/dcrm/settings.py`: configura apps, middleware, base de datos MySQL, archivos estaticos, seguridad, sesiones y CSRF.
- `dcrm/dcrm/urls.py`: conecta `/admin/` y delega la raiz a `website.urls`.
- `dcrm/dcrm/asgi.py`: entrada ASGI del proyecto.
- `dcrm/dcrm/wsgi.py`: entrada WSGI del proyecto.

## App `website`

- `dcrm/website/apps.py`: registra la app y carga `signals.py` en `ready()`.
- `dcrm/website/admin.py`: registra los modelos en Django Admin.
- `dcrm/website/urls.py`: define rutas de autenticacion, registros de clientes y pedidos.
- `dcrm/website/signals.py`: usa señales `pre_save` y `post_save` para crear historial de pedidos.
- `dcrm/website/tests.py`: cubre login, seguridad, roles, validaciones, formularios y calculo de pedidos.

## Modelos

- `dcrm/website/models/record.py`: define `Record`, el modelo de datos de clientes.
- `dcrm/website/models/order.py`: define `Order`, `OrderItem`, `OrderStatusHistory`, `StockReservation` y `OrderView`.
- `dcrm/website/models/__init__.py`: centraliza imports publicos de modelos.

## Formularios

- `dcrm/website/forms/signup_form.py`: personaliza registro de usuarios y validaciones en español.
- `dcrm/website/forms/record_form.py`: formulario para crear o editar clientes.
- `dcrm/website/forms/order_form.py`: formularios de pedido, items y formset.
- `dcrm/website/forms/__init__.py`: centraliza imports publicos de formularios.

## Vistas

- `dcrm/website/views/auth_views.py`: contiene home, login, logout, registro y manejo de error CSRF.
- `dcrm/website/views/record_views.py`: contiene detalle, eliminacion y actualizacion de clientes.
- `dcrm/website/views/order_views.py`: contiene listado, creacion, edicion y eliminacion de pedidos.
- `dcrm/website/views/helpers.py`: centraliza roles, redireccion post-login y paginacion.
- `dcrm/website/views/__init__.py`: expone las vistas para `website.urls`.

## Plantillas y estaticos

- `dcrm/website/templates/base.html`: layout base.
- `dcrm/website/templates/navbar.html`: navegacion comun.
- `dcrm/website/templates/home.html`: dashboard autenticado de registros.
- `dcrm/website/templates/login.html`: formulario de inicio de sesion.
- `dcrm/website/templates/register.html`: formulario de registro.
- `dcrm/website/templates/record.html`: detalle de cliente.
- `dcrm/website/templates/update_record.html`: edicion de cliente.
- `dcrm/website/templates/orders/order_list.html`: listado de pedidos.
- `dcrm/website/templates/orders/order_form.html`: creacion y edicion de pedidos.
- `dcrm/website/templates/orders/order_confirm_delete.html`: confirmacion de eliminacion.
- `dcrm/website/templates/orders/partials/order_field.html`: render reutilizable de campos de pedido.
- `dcrm/website/templates/orders/partials/order_item_form.html`: fila reutilizable para items de pedido.
- `dcrm/website/templates/partials/auth_brand_panel.html`: bloque visual compartido de autenticacion.
- `dcrm/website/templates/static/css/*.css`: estilos locales por pantalla.
- `dcrm/website/templates/static/js/*.js`: scripts locales de base, autenticacion y pedidos.

## Migraciones

- `dcrm/website/migrations/0001_initial.py`: migracion inicial de clientes.
- `dcrm/website/migrations/0002_order_orderitem_orderstatushistory_orderview_and_more.py`: migracion de pedidos, items, historial, reservas y visualizaciones.
- `dcrm/website/migrations/__init__.py`: marca el paquete de migraciones.
