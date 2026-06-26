# Documentación Técnica y Manual de Usuario

## 1. Información general del sistema

| Campo                      | Valor                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| **Nombre del sistema**     | AngelowDjangoOrders                                                                               |
| **Tipo de sistema**        | Aplicación web Django para gestión de clientes, pedidos, productos, reservas de stock y auditoría |
| **Arquitectura principal** | Django MTV: Models, Templates, Views                                                              |
| **Autor(es)**              | Braian551 / propietario del repositorio                                                           |
| **Fecha de documentación** | Junio 2026                                                                                        |
| **Versión documentada**    | v1.0 - estado actual del repositorio                                                              |
| **Repositorio**            | https://github.com/Braian551/AngelowDjangoOrders                                                  |
| **URL local**              | http://127.0.0.1:8000/                                                                            |
| **Panel administrativo**   | http://127.0.0.1:8000/admin/                                                                      |
| **Base de datos**          | MySQL 8.4, base `clientes`                                                                        |
| **Modelo de IA**           | No aplica. El proyecto no implementa Machine Learning ni IA generativa.                           |

---

## 2. Resumen ejecutivo

AngelowDjangoOrders es un sistema web desarrollado con Django para administrar usuarios, clientes y pedidos. El sistema permite autenticación, registro de usuarios, redirección según rol, consulta de clientes, gestión administrativa de pedidos, registro de ítems por pedido, cálculo automático de totales, sincronización de reservas de stock y auditoría de cambios de estado.

La aplicación está orientada a escenarios académicos o empresariales pequeños donde se necesita centralizar datos de clientes y pedidos en una interfaz web sencilla. El backend usa Django 5.2.8, persistencia MySQL, plantillas HTML con Bootstrap local, validaciones con formularios Django y pruebas automatizadas con `TestCase`.

El proyecto también incluye documentación arquitectónica en imágenes C4/UML y un documento de patrones de diseño que identifica el uso de Observer, Decorator, State, Factory Method, Strategy, Facade, Template Method, MTV, ORM/Active Record y ModelForm/Form Object.

---

## 3. Problema y contexto

### 3.1 Problema identificado

En una operación de pedidos, los datos de clientes, órdenes, productos y estados pueden quedar dispersos o ser gestionados manualmente. Esto dificulta consultar información actualizada, controlar cambios de estado, calcular totales de forma consistente y mantener trazabilidad sobre pedidos y reservas.

### 3.2 Justificación del sistema

El sistema centraliza la gestión en una aplicación web con roles, formularios validados y persistencia relacional. Django permite separar responsabilidades, reutilizar componentes y reducir errores frecuentes en operaciones CRUD, autenticación, autorización y validación de datos.

### 3.3 Alcance funcional

* Registro, inicio y cierre de sesión.
* Redirección por rol: administrador hacia pedidos y cliente hacia dashboard.
* Consulta, edición y eliminación de registros de clientes desde la interfaz actual.
* Creación, listado, edición y eliminación de pedidos para usuarios administradores.
* Registro de varios productos dentro de un pedido mediante formsets.
* Cálculo automático del total del pedido desde cantidad y precio unitario.
* Sincronización de reservas de stock asociadas a ítems.
* Historial automático de cambios de estado y estado de pago.
* Registro de visualizaciones de pedidos.
* Panel administrativo nativo de Django para gestionar todos los modelos.

---

## 4. Arquitectura del sistema

### 4.1 Estilo arquitectónico

El proyecto usa el patrón arquitectónico MTV de Django:

| Capa      | Ubicación                                   | Responsabilidad                                           |
| --------- | ------------------------------------------- | --------------------------------------------------------- |
| Models    | `dcrm/website/models/`                      | Entidades, relaciones, reglas de dominio y persistencia   |
| Templates | `dcrm/website/templates/`                   | Interfaz HTML renderizada en servidor                     |
| Views     | `dcrm/website/views/`                       | Coordinación HTTP, permisos, formularios y respuestas     |
| Forms     | `dcrm/website/forms/`                       | Validación de entrada, widgets y mensajes de error        |
| Signals   | `dcrm/website/signals.py`                   | Auditoría automática de cambios en pedidos                |
| URLs      | `dcrm/dcrm/urls.py`, `dcrm/website/urls.py` | Enrutamiento global y de la app                           |
| Settings  | `dcrm/dcrm/settings.py`                     | Configuración global, base de datos, seguridad y sesiones |

### 4.2 Flujo general

```text
Navegador
    -> URL Router de Django
    -> Vista de website
    -> Formulario Django, si hay entrada de usuario
    -> Modelo Django / ORM
    -> Base de datos MySQL
    -> Template HTML + Bootstrap
    -> Respuesta al navegador
```

### 4.3 Flujo de autenticación

```text
Usuario abre /
    -> Si no tiene sesión: redirección a /login/
    -> Ingresa usuario y contraseña
    -> Django autentica credenciales
    -> Si es staff o superusuario: redirección a /orders/
    -> Si es cliente normal: redirección a /
```

### 4.4 Flujo de creación de pedido

```text
Admin abre /orders/create/
    -> Sistema muestra OrderForm + OrderItemFormSet
    -> Admin ingresa número, estado, pago y productos
    -> Backend valida formulario padre e ítems
    -> Guarda Order
    -> Guarda OrderItem asociados
    -> Sincroniza StockReservation
    -> Calcula total desde ítems
    -> Signals crean historial inicial
    -> Redirección a /orders/
```

### 4.5 Flujo de actualización de pedido

```text
Admin abre /orders/<id>/edit/
    -> Sistema registra OrderView
    -> Muestra datos actuales del pedido e ítems
    -> Admin modifica pedido o productos
    -> Backend valida y guarda cambios
    -> Signals comparan estado anterior contra estado nuevo
    -> Si cambió estado o pago, crea OrderStatusHistory
    -> Sincroniza reservas y recalcula total
    -> Redirección a /orders/
```

---

## 5. Modelo de datos

### 5.1 Entidades principales

| Modelo               | Propósito                                   | Archivo                         |
| -------------------- | ------------------------------------------- | ------------------------------- |
| `Record`             | Guarda información básica de clientes       | `dcrm/website/models/record.py` |
| `Order`              | Representa un pedido                        | `dcrm/website/models/order.py`  |
| `OrderItem`          | Representa un producto dentro de un pedido  | `dcrm/website/models/order.py`  |
| `OrderStatusHistory` | Registra cambios de estado y estado de pago | `dcrm/website/models/order.py`  |
| `StockReservation`   | Reserva de stock asociada a un ítem         | `dcrm/website/models/order.py`  |
| `OrderView`          | Registro de visualización de un pedido      | `dcrm/website/models/order.py`  |

### 5.2 Campos por entidad

#### Record

| Campo          | Tipo            | Descripción                  |
| -------------- | --------------- | ---------------------------- |
| `created_at`   | DateTime        | Fecha de creación automática |
| `first_name`   | CharField(50)   | Nombre del cliente           |
| `last_name`    | CharField(50)   | Apellido del cliente         |
| `email`        | EmailField(100) | Correo electrónico           |
| `phone_number` | CharField(15)   | Teléfono                     |
| `address`      | CharField(255)  | Dirección                    |
| `city`         | CharField(50)   | Ciudad                       |
| `state`        | CharField(50)   | Estado/departamento          |
| `zip_code`     | CharField(10)   | Código postal                |

#### Order

| Campo            | Tipo                 | Descripción                                       |
| ---------------- | -------------------- | ------------------------------------------------- |
| `order_number`   | CharField(20), único | Número público del pedido                         |
| `status`         | Choice               | `pending`, `processing`, `completed`, `cancelled` |
| `payment_status` | Choice               | `pending`, `paid`, `failed`, `refunded`           |
| `total`          | Decimal(10,2)        | Total calculado desde los ítems                   |
| `created_at`     | DateTime             | Fecha de creación                                 |
| `updated_at`     | DateTime             | Fecha de última actualización                     |

#### OrderItem

| Campo          | Tipo            | Descripción             |
| -------------- | --------------- | ----------------------- |
| `order`        | ForeignKey      | Pedido padre            |
| `product_name` | CharField(100)  | Nombre del producto     |
| `quantity`     | PositiveInteger | Cantidad solicitada     |
| `unit_price`   | Decimal(10,2)   | Precio unitario         |
| `subtotal`     | Property        | `quantity * unit_price` |

#### OrderStatusHistory

| Campo                     | Tipo           | Descripción                |
| ------------------------- | -------------- | -------------------------- |
| `order`                   | ForeignKey     | Pedido auditado            |
| `previous_status`         | Choice         | Estado anterior del pedido |
| `new_status`              | Choice         | Estado nuevo del pedido    |
| `previous_payment_status` | Choice         | Estado anterior del pago   |
| `new_payment_status`      | Choice         | Estado nuevo del pago      |
| `note`                    | CharField(255) | Nota del movimiento        |
| `changed_at`              | DateTime       | Fecha del cambio           |

#### StockReservation

| Campo          | Tipo            | Descripción                       |
| -------------- | --------------- | --------------------------------- |
| `order`        | ForeignKey      | Pedido relacionado                |
| `order_item`   | OneToOneField   | Ítem relacionado                  |
| `product_name` | CharField(100)  | Producto reservado                |
| `quantity`     | PositiveInteger | Cantidad reservada                |
| `status`       | Choice          | `reserved`, `expired`, `released` |
| `created_at`   | DateTime        | Fecha de creación                 |
| `updated_at`   | DateTime        | Fecha de actualización            |

#### OrderView

| Campo       | Tipo           | Descripción                          |
| ----------- | -------------- | ------------------------------------ |
| `order`     | ForeignKey     | Pedido visto                         |
| `viewed_by` | CharField(150) | Nombre del usuario que vio el pedido |
| `viewed_at` | DateTime       | Fecha de visualización               |

---

## 6. Funcionalidades por módulo

### 6.1 Autenticación

| Función             | Descripción                                                   |
| ------------------- | ------------------------------------------------------------- |
| Login               | Valida usuario y contraseña mediante `authenticate()`         |
| Logout              | Cierra sesión con `logout()`                                  |
| Registro            | Crea usuario con `SignUpForm` y lo autentica automáticamente  |
| Redirección por rol | Admin a `orders`; cliente a `home`                            |
| CSRF personalizado  | Redirección a login con mensaje claro si el formulario expira |

### 6.2 Clientes

| Función     | Descripción                                                     |
| ----------- | --------------------------------------------------------------- |
| Dashboard   | Lista registros paginados de clientes                           |
| Detalle     | Muestra información de un cliente                               |
| Edición     | Actualiza cliente con `RecordForm`                              |
| Eliminación | Elimina registro de cliente autenticado                         |
| Creación    | No existe ruta pública actual; puede hacerse desde Django Admin |

### 6.3 Pedidos

| Función      | Descripción                                           |
| ------------ | ----------------------------------------------------- |
| Listado      | Muestra pedidos con productos y total                 |
| Creación     | Crea pedido e ítems desde un único formulario         |
| Edición      | Actualiza estado, pago e ítems                        |
| Eliminación  | Requiere confirmación por POST                        |
| Total        | Se calcula en backend con `Order.calculate_total()`   |
| Vista previa | JS calcula un total visual antes de guardar           |
| Reservas     | `sync_stock_reservations()` crea o actualiza reservas |
| Auditoría    | Signals registran historial de creación y cambios     |

---

## 7. Rutas del sistema

| Ruta                         | Vista             | Acceso              | Descripción                |
| ---------------------------- | ----------------- | ------------------- | -------------------------- |
| `/`                          | `home`            | Usuario autenticado | Dashboard de registros     |
| `/login/`                    | `login_user`      | Público             | Inicio de sesión           |
| `/logout/`                   | `logout_user`     | Usuario autenticado | Cierre de sesión           |
| `/registrar/`                | `register_user`   | Público             | Registro de usuario        |
| `/record/<pk>/`              | `customer_record` | Usuario autenticado | Detalle de cliente         |
| `/delete_record/<pk>/`       | `delete_record`   | Usuario autenticado | Eliminación de cliente     |
| `/update_record/<pk>/`       | `update_record`   | Usuario autenticado | Edición de cliente         |
| `/orders/`                   | `list_orders`     | Admin               | Listado de pedidos         |
| `/orders/create/`            | `create_order`    | Admin               | Creación de pedido         |
| `/orders/<order_id>/edit/`   | `update_order`    | Admin               | Edición de pedido          |
| `/orders/<order_id>/delete/` | `delete_order`    | Admin               | Confirmación y eliminación |
| `/admin/`                    | Django Admin      | Staff/superuser     | Administración nativa      |

---

## 8. Formularios y validaciones

### 8.1 SignUpForm

Archivo: `dcrm/website/forms/signup_form.py`

Campos:

* `username`
* `first_name`
* `last_name`
* `email`
* `password1`
* `password2`

Validaciones destacadas:

* Usuario con letras, números y caracteres `. _ + -`.
* Nombre y apellido solo con letras y espacios.
* Contraseña con lista segura de caracteres.
* Confirmación obligatoria de contraseña.
* Mensajes de error personalizados en español.

### 8.2 RecordForm

Archivo: `dcrm/website/forms/record_form.py`

Campos:

* `first_name`
* `last_name`
* `email`
* `phone_number`
* `address`
* `city`
* `state`
* `zip_code`

Validaciones destacadas:

* Nombres y ciudades solo con letras y espacios.
* Teléfono con números, espacios, `+` y `-`.
* Dirección con caracteres controlados.
* Código postal alfanumérico con guion.

### 8.3 OrderForm

Archivo: `dcrm/website/forms/order_form.py`

Campos:

* `order_number`
* `status`
* `payment_status`

Validaciones destacadas:

* Número de pedido único sin diferenciar mayúsculas/minúsculas.
* Número de pedido solo con letras, números y guion.
* Estados limitados por `choices`.
* El campo `total` no se expone al usuario porque se calcula desde ítems.

### 8.4 OrderItemForm y OrderItemFormSet

Campos:

* `product_name`
* `quantity`
* `unit_price`

Reglas:

* Las filas vacías se permiten.
* Si el usuario empieza a llenar una fila, debe completar producto, cantidad y precio.
* La cantidad debe ser mayor a cero.
* El precio unitario no puede ser negativo.
* Se usa `inlineformset_factory()` para manejar varios ítems en un pedido.

---

## 9. Patrones de diseño identificados

| Patrón                  | Tipo                         | Evidencia en el proyecto                                                       |
| ----------------------- | ---------------------------- | ------------------------------------------------------------------------------ |
| Observer                | GoF comportamiento           | `signals.py` escucha `pre_save` y `post_save` de `Order`                       |
| Decorator               | GoF estructural              | `login_required`, `user_passes_test`, `never_cache`, `ensure_csrf_cookie`      |
| State                   | GoF aplicado de forma simple | Estados con `choices` en `Order` y `StockReservation`                          |
| Factory Method          | GoF aplicado con helper      | `inlineformset_factory()` crea `OrderItemFormSet`                              |
| Strategy                | GoF comportamiento simple    | `is_admin_user()` y `get_login_redirect_url()`                                 |
| Facade                  | Estructural                  | Vistas de pedidos coordinan formularios, modelos, mensajes, reservas y totales |
| Template Method         | GoF vía Django Forms         | `is_valid()` ejecuta `clean_*()` y `clean()`                                   |
| MTV                     | Arquitectónico Django        | Separación Models, Templates y Views                                           |
| ORM / Active Record     | Persistencia                 | Modelos heredan de `models.Model` y usan `objects`                             |
| ModelForm / Form Object | Convención Django            | Formularios encapsulan entrada, validación y guardado                          |

Documento relacionado: `docs/patrones/patrones_diseno.md`

---

## 10. Implementación técnica

### 10.1 Stack tecnológico

| Capa                 | Tecnología                   | Versión / detalle          |
| -------------------- | ---------------------------- | -------------------------- |
| Lenguaje             | Python                       | 3.14 en Dockerfile         |
| Framework            | Django                       | 5.2.8                      |
| Base de datos        | MySQL                        | 8.4 en Docker Compose      |
| Driver DB            | PyMySQL                      | 1.1.2                      |
| Cifrado/dependencia  | cryptography                 | 46.0.3                     |
| Variables de entorno | python-dotenv                | 1.0.1                      |
| SQL utilities        | sqlparse                     | 0.4.4                      |
| UI                   | Django Templates + Bootstrap | Bootstrap local            |
| Contenedores         | Docker + Docker Compose      | Servicio web y servicio db |
| Pruebas              | Django TestCase              | `dcrm/website/tests.py`    |

### 10.2 Estructura principal

```text
AngelowDjangoOrders/
|-- dcrm/
|   |-- manage.py
|   |-- dcrm/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- asgi.py
|   |   `-- wsgi.py
|   `-- website/
|       |-- admin.py
|       |-- apps.py
|       |-- signals.py
|       |-- tests.py
|       |-- urls.py
|       |-- forms/
|       |-- models/
|       |-- views/
|       `-- templates/
|-- docker/
|   `-- entrypoint.sh
|-- docs/
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- README.md
```

### 10.3 Configuración de base de datos

La configuración vive en `dcrm/dcrm/settings.py`.

Variables soportadas:

| Variable             | Valor por defecto | Uso                      |
| -------------------- | ----------------- | ------------------------ |
| `DJANGO_DB_NAME`     | `clientes`        | Nombre de la base        |
| `DJANGO_DB_USER`     | `root`            | Usuario de base de datos |
| `DJANGO_DB_PASSWORD` | vacío             | Contraseña               |
| `DJANGO_DB_HOST`     | `localhost`       | Host de base de datos    |
| `DJANGO_DB_PORT`     | `3306`            | Puerto                   |

En Docker Compose:

| Servicio | Puerto      | Función           |
| -------- | ----------- | ----------------- |
| `web`    | `8000:8000` | Aplicación Django |
| `db`     | `3307:3306` | MySQL 8.4         |

### 10.4 Arranque con Docker

El entrypoint ejecuta migraciones y luego inicia el servidor:

```sh
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
```

---

## 11. Seguridad

| Mecanismo             | Implementación                                                    |
| --------------------- | ----------------------------------------------------------------- |
| Autenticación         | `authenticate()`, `login()`, `logout()`                           |
| Autorización por rol  | Admin si `is_staff` o `is_superuser`                              |
| Protección de pedidos | `login_required` + `user_passes_test(is_admin_user)`              |
| CSRF                  | Middleware de Django + tokens en formularios                      |
| Error CSRF legible    | `CSRF_FAILURE_VIEW = 'website.views.csrf_failure'`                |
| Cookies               | `SESSION_COOKIE_HTTPONLY`, `CSRF_COOKIE_HTTPONLY`, `SameSite=Lax` |
| Clickjacking          | `X_FRAME_OPTIONS = 'DENY'`                                        |
| MIME sniffing         | `SECURE_CONTENT_TYPE_NOSNIFF = True`                              |
| Validación de entrada | Regex y validaciones en formularios                               |
| Auditoría             | `OrderStatusHistory` vía signals                                  |

### 11.1 Consideraciones de producción

El estado actual está preparado principalmente para desarrollo local:

* `DEBUG = True`.
* `SECRET_KEY` está escrita directamente en `settings.py`.
* `ALLOWED_HOSTS` solo permite `127.0.0.1` y `localhost` cuando `DEBUG=True`.
* No hay configuración de archivos estáticos para producción con `collectstatic`.
* Se recomienda mover secretos y configuración sensible a variables de entorno antes de desplegar.

---

## 12. Pruebas y validación

Archivo principal: `dcrm/website/tests.py`

### 12.1 Cobertura funcional observada

| Área            | Pruebas existentes                                      |
| --------------- | ------------------------------------------------------- |
| Login           | Formulario, autenticación y persistencia de sesión      |
| Roles           | Admin redirige a pedidos; cliente no accede a pedidos   |
| CSRF            | Vista personalizada ante POST sin token válido          |
| Seguridad local | Cookies seguras desactivadas en desarrollo HTTP         |
| Registro        | Mensajes en español, regex y confirmación de contraseña |
| Clientes        | Validación de caracteres en `RecordForm`                |
| Pedidos         | Campos obligatorios, número único, regex, ítems y total |
| UI de pedidos   | Botones para agregar/quitar productos                   |

### 12.2 Comandos recomendados

```powershell
cd dcrm
python manage.py check
python manage.py test website
```

### 12.3 Brechas de pruebas

Actualmente no se observan pruebas específicas para:

* Creación de `OrderStatusHistory` mediante signals.
* Sincronización de `StockReservation`.
* Registro de `OrderView`.
* Eliminación de pedidos y clientes.
* Render correcto de detalle de cliente con todos los campos actuales.

---

## 13. Instalación y ejecución

### 13.1 Requisitos

Opción Docker:

* Docker
* Docker Compose

Opción local:

* Python compatible con Django 5.2
* MySQL o MariaDB
* `pip`
* Entorno virtual recomendado

### 13.2 Ejecución con Docker

```powershell
docker compose up -d --build
docker compose ps
```

Abrir:

```text
http://127.0.0.1:8000/
```

### 13.3 Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:DJANGO_DB_NAME="clientes"
$env:DJANGO_DB_USER="root"
$env:DJANGO_DB_PASSWORD=""
$env:DJANGO_DB_HOST="localhost"
$env:DJANGO_DB_PORT="3306"

cd dcrm
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 14. Manual de usuario

### 14.1 Iniciar sesión

1. Abrir `http://127.0.0.1:8000/`.
2. Si no hay sesión activa, el sistema redirige a `/login/`.
3. Ingresar usuario y contraseña.
4. Presionar **Entrar**.
5. El sistema redirige según el rol:

   * Admin: módulo de pedidos.
   * Cliente: dashboard principal.

### 14.2 Registrar usuario

1. Abrir `/registrar/`.
2. Completar usuario, nombre, apellido, correo, contraseña y confirmación.
3. Presionar **Registrar**.
4. Si los datos son válidos, el sistema crea la cuenta e inicia sesión.
5. Los usuarios nuevos quedan como clientes normales. Para convertirlos en Admin se debe editar `is_staff` o `is_superuser` desde Django Admin.

### 14.3 Consultar dashboard de clientes

1. Iniciar sesión.
2. Abrir `/` o seleccionar **Dashboard**.
3. Revisar la tabla de clientes registrados.
4. Usar la paginación cuando existan más de 8 registros.
5. Presionar **Ver** para abrir el detalle de un cliente.

### 14.4 Editar cliente

1. Desde el dashboard, presionar **Ver** en un cliente.
2. Presionar **Update Record**.
3. Modificar los campos necesarios.
4. Presionar **Actualizar**.
5. El sistema valida los datos y vuelve al dashboard si la actualización es correcta.

### 14.5 Eliminar cliente

1. Desde el detalle del cliente, presionar **Delete**.
2. El sistema elimina el registro directamente.
3. Se muestra un mensaje de éxito y se vuelve al dashboard.

Nota: en la versión actual la eliminación de clientes no tiene pantalla de confirmación previa y se ejecuta desde un enlace GET.

---

## 15. Manual de administrador

### 15.1 Acceder al módulo de pedidos

1. Iniciar sesión con un usuario `staff` o `superuser`.
2. El sistema redirige automáticamente a `/orders/`.
3. También se puede entrar desde el menú **Gestión > Listado de pedidos**.

### 15.2 Crear pedido

1. Abrir `/orders/create/` o presionar **Crear pedido**.
2. Ingresar:

   * Número de pedido.
   * Estado del pedido.
   * Estado de pago.
3. Agregar uno o más productos:

   * Producto.
   * Cantidad.
   * Precio unitario.
4. Usar **Agregar producto** para crear más filas.
5. Revisar el total calculado en pantalla.
6. Presionar **Guardar pedido**.
7. El backend recalcula el total, crea reservas de stock y registra historial inicial.

### 15.3 Editar pedido

1. En `/orders/`, presionar **Editar**.
2. Cambiar datos generales, estado de pedido, estado de pago o productos.
3. Para quitar un producto, presionar **Quitar** o **Eliminar** en la fila.
4. Presionar **Actualizar pedido**.
5. Si cambia estado o pago, se registra una entrada en el historial.
6. Se recalculan total y reservas.

### 15.4 Eliminar pedido

1. En `/orders/`, presionar **Eliminar**.
2. Revisar la pantalla de confirmación.
3. Presionar **Sí, eliminar pedido**.
4. El pedido se elimina por POST y el sistema vuelve al listado.

### 15.5 Administrar desde Django Admin

1. Crear un superusuario:

```powershell
cd dcrm
python manage.py createsuperuser
```

2. Abrir `/admin/`.
3. Iniciar sesión con el superusuario.
4. Gestionar:

   * Usuarios.
   * Records.
   * Orders.
   * OrderItems.
   * OrderStatusHistory.
   * StockReservation.
   * OrderView.

---

## 16. Resultados y valor del sistema

* Centraliza información de clientes y pedidos.
* Aplica roles para separar usuario cliente y administrador.
* Reduce errores de entrada con formularios validados.
* Evita edición manual del total de pedido.
* Mantiene trazabilidad de cambios de estado.
* Permite trabajar con múltiples productos por pedido.
* Usa Docker para facilitar ejecución reproducible.
* Incluye diagramas y patrones de diseño como soporte académico/técnico.

---

## 17. Limitaciones y hallazgos técnicos

| Hallazgo                                              | Impacto                                                         | Recomendación                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `DEBUG=True` en `settings.py`                         | No apto para producción                                         | Mover a variable de entorno                                                |
| `SECRET_KEY` hardcodeada                              | Riesgo de seguridad en despliegue real                          | Usar variable de entorno                                                   |
| No hay ruta pública para crear `Record`               | CRUD de clientes incompleto desde interfaz web                  | Agregar vista `create_record` si se requiere CRUD completo                 |
| `record.html` usa `phone` y `zipcode`                 | El detalle puede no mostrar teléfono/código postal actuales     | Cambiar a `phone_number` y `zip_code`                                      |
| `update_record.html` tiene estructura HTML incompleta | Puede afectar renderizado o estilo                              | Cerrar correctamente formulario/divs                                       |
| Eliminación de cliente por GET y sin confirmación     | Riesgo de borrado accidental o acción destructiva sin CSRF POST | Agregar pantalla de confirmación y eliminar solo por POST                  |
| Pruebas sin signals/reservas/vistas                   | Riesgo de regresión en auditoría                                | Agregar pruebas para `OrderStatusHistory`, `StockReservation`, `OrderView` |
| No hay despliegue público documentado                 | Entrega limitada a local/Docker                                 | Agregar guía de despliegue                                                 |

---

## 18. Ética, privacidad y seguridad de datos

* El sistema almacena datos personales básicos de clientes: nombre, correo, teléfono y dirección.
* Se recomienda limitar acceso a usuarios autorizados.
* En producción se debe usar HTTPS.
* Se debe proteger la base de datos con credenciales robustas.
* Se recomienda establecer políticas de respaldo y retención de datos.
* No se detecta almacenamiento de datos de tarjetas, documentos oficiales ni información financiera sensible.
* El proyecto no toma decisiones automatizadas con IA; por tanto, no aplica evaluación de sesgo algorítmico.

---

## 19. Checklist de entrega

* [x] Documentación técnica del sistema.
* [x] Manual de usuario.
* [x] Manual de administrador.
* [x] Descripción de arquitectura.
* [x] Modelo de datos.
* [x] Rutas del sistema.
* [x] Seguridad y validaciones.
* [x] Instalación local y Docker.
* [x] Pruebas existentes y brechas.
* [x] Limitaciones y recomendaciones.

**Repositorio:**

* GitHub: https://github.com/Braian551/AngelowDjangoOrders

**Documentos relacionados:**

* `README.md`
* `docs/patrones/patrones_diseno.md`
* `docs/arquitectura/c1.png`
* `docs/arquitectura/c2.png`
* `docs/arquitectura/c3.png`
* `docs/arquitectura/c4.png`
* `docs/Diagrama de clases.png`
