# Documentacion Tecnica y Manual de Usuario

## 1. Informacion general del sistema

| Campo | Valor |
|-------|-------|
| **Nombre del sistema** | AngelowDjangoOrders |
| **Tipo de sistema** | Aplicacion web Django para gestion de clientes, pedidos, productos, reservas de stock y auditoria |
| **Arquitectura principal** | Django MTV: Models, Templates, Views |
| **Autor(es)** | Braian551 / propietario del repositorio |
| **Fecha de documentacion** | Junio 2026 |
| **Version documentada** | v1.0 - estado actual del repositorio |
| **Repositorio** | https://github.com/Braian551/AngelowDjangoOrders |
| **URL local** | http://127.0.0.1:8000/ |
| **Panel administrativo** | http://127.0.0.1:8000/admin/ |
| **Base de datos** | MySQL 8.4, base `clientes` |
| **Modelo de IA** | No aplica. El proyecto no implementa Machine Learning ni IA generativa. |

---

## 2. Resumen ejecutivo

AngelowDjangoOrders es un sistema web desarrollado con Django para administrar usuarios, clientes y pedidos. El sistema permite autenticacion, registro de usuarios, redireccion segun rol, consulta de clientes, gestion administrativa de pedidos, registro de items por pedido, calculo automatico de totales, sincronizacion de reservas de stock y auditoria de cambios de estado.

La aplicacion esta orientada a escenarios academicos o empresariales pequenos donde se necesita centralizar datos de clientes y pedidos en una interfaz web sencilla. El backend usa Django 5.2.8, persistencia MySQL, plantillas HTML con Bootstrap local, validaciones con formularios Django y pruebas automatizadas con `TestCase`.

El proyecto tambien incluye documentacion arquitectonica en imagenes C4/UML y un documento de patrones de diseno que identifica el uso de Observer, Decorator, State, Factory Method, Strategy, Facade, Template Method, MTV, ORM/Active Record y ModelForm/Form Object.

---

## 3. Problema y contexto

### 3.1 Problema identificado

En una operacion de pedidos, los datos de clientes, ordenes, productos y estados pueden quedar dispersos o ser gestionados manualmente. Esto dificulta consultar informacion actualizada, controlar cambios de estado, calcular totales de forma consistente y mantener trazabilidad sobre pedidos y reservas.

### 3.2 Justificacion del sistema

El sistema centraliza la gestion en una aplicacion web con roles, formularios validados y persistencia relacional. Django permite separar responsabilidades, reutilizar componentes y reducir errores frecuentes en operaciones CRUD, autenticacion, autorizacion y validacion de datos.

### 3.3 Alcance funcional

- Registro, inicio y cierre de sesion.
- Redireccion por rol: administrador hacia pedidos y cliente hacia dashboard.
- Consulta, edicion y eliminacion de registros de clientes desde la interfaz actual.
- Creacion, listado, edicion y eliminacion de pedidos para usuarios administradores.
- Registro de varios productos dentro de un pedido mediante formsets.
- Calculo automatico del total del pedido desde cantidad y precio unitario.
- Sincronizacion de reservas de stock asociadas a items.
- Historial automatico de cambios de estado y estado de pago.
- Registro de visualizaciones de pedidos.
- Panel administrativo nativo de Django para gestionar todos los modelos.

---

## 4. Arquitectura del sistema

### 4.1 Estilo arquitectonico

El proyecto usa el patron arquitectonico MTV de Django:

| Capa | Ubicacion | Responsabilidad |
|------|-----------|-----------------|
| Models | `dcrm/website/models/` | Entidades, relaciones, reglas de dominio y persistencia |
| Templates | `dcrm/website/templates/` | Interfaz HTML renderizada en servidor |
| Views | `dcrm/website/views/` | Coordinacion HTTP, permisos, formularios y respuestas |
| Forms | `dcrm/website/forms/` | Validacion de entrada, widgets y mensajes de error |
| Signals | `dcrm/website/signals.py` | Auditoria automatica de cambios en pedidos |
| URLs | `dcrm/dcrm/urls.py`, `dcrm/website/urls.py` | Enrutamiento global y de la app |
| Settings | `dcrm/dcrm/settings.py` | Configuracion global, base de datos, seguridad y sesiones |

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

### 4.3 Flujo de autenticacion

```text
Usuario abre /
    -> Si no tiene sesion: redireccion a /login/
    -> Ingresa usuario y contrasena
    -> Django autentica credenciales
    -> Si es staff o superusuario: redireccion a /orders/
    -> Si es cliente normal: redireccion a /
```

### 4.4 Flujo de creacion de pedido

```text
Admin abre /orders/create/
    -> Sistema muestra OrderForm + OrderItemFormSet
    -> Admin ingresa numero, estado, pago y productos
    -> Backend valida formulario padre e items
    -> Guarda Order
    -> Guarda OrderItem asociados
    -> Sincroniza StockReservation
    -> Calcula total desde items
    -> Signals crean historial inicial
    -> Redireccion a /orders/
```

### 4.5 Flujo de actualizacion de pedido

```text
Admin abre /orders/<id>/edit/
    -> Sistema registra OrderView
    -> Muestra datos actuales del pedido e items
    -> Admin modifica pedido o productos
    -> Backend valida y guarda cambios
    -> Signals comparan estado anterior contra estado nuevo
    -> Si cambio estado o pago, crea OrderStatusHistory
    -> Sincroniza reservas y recalcula total
    -> Redireccion a /orders/
```

---

## 5. Modelo de datos

### 5.1 Entidades principales

| Modelo | Proposito | Archivo |
|--------|-----------|---------|
| `Record` | Guarda informacion basica de clientes | `dcrm/website/models/record.py` |
| `Order` | Representa un pedido | `dcrm/website/models/order.py` |
| `OrderItem` | Representa un producto dentro de un pedido | `dcrm/website/models/order.py` |
| `OrderStatusHistory` | Registra cambios de estado y estado de pago | `dcrm/website/models/order.py` |
| `StockReservation` | Reserva de stock asociada a un item | `dcrm/website/models/order.py` |
| `OrderView` | Registro de visualizacion de un pedido | `dcrm/website/models/order.py` |

### 5.2 Campos por entidad

#### Record

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `created_at` | DateTime | Fecha de creacion automatica |
| `first_name` | CharField(50) | Nombre del cliente |
| `last_name` | CharField(50) | Apellido del cliente |
| `email` | EmailField(100) | Correo electronico |
| `phone_number` | CharField(15) | Telefono |
| `address` | CharField(255) | Direccion |
| `city` | CharField(50) | Ciudad |
| `state` | CharField(50) | Estado/departamento |
| `zip_code` | CharField(10) | Codigo postal |

#### Order

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order_number` | CharField(20), unico | Numero publico del pedido |
| `status` | Choice | `pending`, `processing`, `completed`, `cancelled` |
| `payment_status` | Choice | `pending`, `paid`, `failed`, `refunded` |
| `total` | Decimal(10,2) | Total calculado desde los items |
| `created_at` | DateTime | Fecha de creacion |
| `updated_at` | DateTime | Fecha de ultima actualizacion |

#### OrderItem

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order` | ForeignKey | Pedido padre |
| `product_name` | CharField(100) | Nombre del producto |
| `quantity` | PositiveInteger | Cantidad solicitada |
| `unit_price` | Decimal(10,2) | Precio unitario |
| `subtotal` | Property | `quantity * unit_price` |

#### OrderStatusHistory

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order` | ForeignKey | Pedido auditado |
| `previous_status` | Choice | Estado anterior del pedido |
| `new_status` | Choice | Estado nuevo del pedido |
| `previous_payment_status` | Choice | Estado anterior del pago |
| `new_payment_status` | Choice | Estado nuevo del pago |
| `note` | CharField(255) | Nota del movimiento |
| `changed_at` | DateTime | Fecha del cambio |

#### StockReservation

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order` | ForeignKey | Pedido relacionado |
| `order_item` | OneToOneField | Item relacionado |
| `product_name` | CharField(100) | Producto reservado |
| `quantity` | PositiveInteger | Cantidad reservada |
| `status` | Choice | `reserved`, `expired`, `released` |
| `created_at` | DateTime | Fecha de creacion |
| `updated_at` | DateTime | Fecha de actualizacion |

#### OrderView

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order` | ForeignKey | Pedido visto |
| `viewed_by` | CharField(150) | Nombre del usuario que vio el pedido |
| `viewed_at` | DateTime | Fecha de visualizacion |

---

## 6. Funcionalidades por modulo

### 6.1 Autenticacion

| Funcion | Descripcion |
|---------|-------------|
| Login | Valida usuario y contrasena mediante `authenticate()` |
| Logout | Cierra sesion con `logout()` |
| Registro | Crea usuario con `SignUpForm` y lo autentica automaticamente |
| Redireccion por rol | Admin a `orders`; cliente a `home` |
| CSRF personalizado | Redireccion a login con mensaje claro si el formulario expira |

### 6.2 Clientes

| Funcion | Descripcion |
|---------|-------------|
| Dashboard | Lista registros paginados de clientes |
| Detalle | Muestra informacion de un cliente |
| Edicion | Actualiza cliente con `RecordForm` |
| Eliminacion | Elimina registro de cliente autenticado |
| Creacion | No existe ruta publica actual; puede hacerse desde Django Admin |

### 6.3 Pedidos

| Funcion | Descripcion |
|---------|-------------|
| Listado | Muestra pedidos con productos y total |
| Creacion | Crea pedido e items desde un unico formulario |
| Edicion | Actualiza estado, pago e items |
| Eliminacion | Requiere confirmacion por POST |
| Total | Se calcula en backend con `Order.calculate_total()` |
| Vista previa | JS calcula un total visual antes de guardar |
| Reservas | `sync_stock_reservations()` crea o actualiza reservas |
| Auditoria | Signals registran historial de creacion y cambios |

---

## 7. Rutas del sistema

| Ruta | Vista | Acceso | Descripcion |
|------|-------|--------|-------------|
| `/` | `home` | Usuario autenticado | Dashboard de registros |
| `/login/` | `login_user` | Publico | Inicio de sesion |
| `/logout/` | `logout_user` | Usuario autenticado | Cierre de sesion |
| `/registrar/` | `register_user` | Publico | Registro de usuario |
| `/record/<pk>/` | `customer_record` | Usuario autenticado | Detalle de cliente |
| `/delete_record/<pk>/` | `delete_record` | Usuario autenticado | Eliminacion de cliente |
| `/update_record/<pk>/` | `update_record` | Usuario autenticado | Edicion de cliente |
| `/orders/` | `list_orders` | Admin | Listado de pedidos |
| `/orders/create/` | `create_order` | Admin | Creacion de pedido |
| `/orders/<order_id>/edit/` | `update_order` | Admin | Edicion de pedido |
| `/orders/<order_id>/delete/` | `delete_order` | Admin | Confirmacion y eliminacion |
| `/admin/` | Django Admin | Staff/superuser | Administracion nativa |

---

## 8. Formularios y validaciones

### 8.1 SignUpForm

Archivo: `dcrm/website/forms/signup_form.py`

Campos:

- `username`
- `first_name`
- `last_name`
- `email`
- `password1`
- `password2`

Validaciones destacadas:

- Usuario con letras, numeros y caracteres `. _ + -`.
- Nombre y apellido solo con letras y espacios.
- Contrasena con lista segura de caracteres.
- Confirmacion obligatoria de contrasena.
- Mensajes de error personalizados en espanol.

### 8.2 RecordForm

Archivo: `dcrm/website/forms/record_form.py`

Campos:

- `first_name`
- `last_name`
- `email`
- `phone_number`
- `address`
- `city`
- `state`
- `zip_code`

Validaciones destacadas:

- Nombres y ciudades solo con letras y espacios.
- Telefono con numeros, espacios, `+` y `-`.
- Direccion con caracteres controlados.
- Codigo postal alfanumerico con guion.

### 8.3 OrderForm

Archivo: `dcrm/website/forms/order_form.py`

Campos:

- `order_number`
- `status`
- `payment_status`

Validaciones destacadas:

- Numero de pedido unico sin diferenciar mayusculas/minusculas.
- Numero de pedido solo con letras, numeros y guion.
- Estados limitados por `choices`.
- El campo `total` no se expone al usuario porque se calcula desde items.

### 8.4 OrderItemForm y OrderItemFormSet

Campos:

- `product_name`
- `quantity`
- `unit_price`

Reglas:

- Las filas vacias se permiten.
- Si el usuario empieza a llenar una fila, debe completar producto, cantidad y precio.
- La cantidad debe ser mayor a cero.
- El precio unitario no puede ser negativo.
- Se usa `inlineformset_factory()` para manejar varios items en un pedido.

---

## 9. Patrones de diseno identificados

| Patron | Tipo | Evidencia en el proyecto |
|--------|------|--------------------------|
| Observer | GoF comportamiento | `signals.py` escucha `pre_save` y `post_save` de `Order` |
| Decorator | GoF estructural | `login_required`, `user_passes_test`, `never_cache`, `ensure_csrf_cookie` |
| State | GoF aplicado de forma simple | Estados con `choices` en `Order` y `StockReservation` |
| Factory Method | GoF aplicado con helper | `inlineformset_factory()` crea `OrderItemFormSet` |
| Strategy | GoF comportamiento simple | `is_admin_user()` y `get_login_redirect_url()` |
| Facade | Estructural | Vistas de pedidos coordinan formularios, modelos, mensajes, reservas y totales |
| Template Method | GoF via Django Forms | `is_valid()` ejecuta `clean_*()` y `clean()` |
| MTV | Arquitectonico Django | Separacion Models, Templates y Views |
| ORM / Active Record | Persistencia | Modelos heredan de `models.Model` y usan `objects` |
| ModelForm / Form Object | Convencion Django | Formularios encapsulan entrada, validacion y guardado |

Documento relacionado: `docs/patrones/patrones_diseno.md`

---

## 10. Implementacion tecnica

### 10.1 Stack tecnologico

| Capa | Tecnologia | Version / detalle |
|------|------------|-------------------|
| Lenguaje | Python | 3.14 en Dockerfile |
| Framework | Django | 5.2.8 |
| Base de datos | MySQL | 8.4 en Docker Compose |
| Driver DB | PyMySQL | 1.1.2 |
| Cifrado/dependencia | cryptography | 46.0.3 |
| Variables de entorno | python-dotenv | 1.0.1 |
| SQL utilities | sqlparse | 0.4.4 |
| UI | Django Templates + Bootstrap | Bootstrap local |
| Contenedores | Docker + Docker Compose | Servicio web y servicio db |
| Pruebas | Django TestCase | `dcrm/website/tests.py` |

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

### 10.3 Configuracion de base de datos

La configuracion vive en `dcrm/dcrm/settings.py`.

Variables soportadas:

| Variable | Valor por defecto | Uso |
|----------|-------------------|-----|
| `DJANGO_DB_NAME` | `clientes` | Nombre de la base |
| `DJANGO_DB_USER` | `root` | Usuario de base de datos |
| `DJANGO_DB_PASSWORD` | vacio | Contrasena |
| `DJANGO_DB_HOST` | `localhost` | Host de base de datos |
| `DJANGO_DB_PORT` | `3306` | Puerto |

En Docker Compose:

| Servicio | Puerto | Funcion |
|----------|--------|---------|
| `web` | `8000:8000` | Aplicacion Django |
| `db` | `3307:3306` | MySQL 8.4 |

### 10.4 Arranque con Docker

El entrypoint ejecuta migraciones y luego inicia el servidor:

```sh
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
```

---

## 11. Seguridad

| Mecanismo | Implementacion |
|-----------|----------------|
| Autenticacion | `authenticate()`, `login()`, `logout()` |
| Autorizacion por rol | Admin si `is_staff` o `is_superuser` |
| Proteccion de pedidos | `login_required` + `user_passes_test(is_admin_user)` |
| CSRF | Middleware de Django + tokens en formularios |
| Error CSRF legible | `CSRF_FAILURE_VIEW = 'website.views.csrf_failure'` |
| Cookies | `SESSION_COOKIE_HTTPONLY`, `CSRF_COOKIE_HTTPONLY`, `SameSite=Lax` |
| Clickjacking | `X_FRAME_OPTIONS = 'DENY'` |
| MIME sniffing | `SECURE_CONTENT_TYPE_NOSNIFF = True` |
| Validacion de entrada | Regex y validaciones en formularios |
| Auditoria | `OrderStatusHistory` via signals |

### 11.1 Consideraciones de produccion

El estado actual esta preparado principalmente para desarrollo local:

- `DEBUG = True`.
- `SECRET_KEY` esta escrita directamente en `settings.py`.
- `ALLOWED_HOSTS` solo permite `127.0.0.1` y `localhost` cuando `DEBUG=True`.
- No hay configuracion de archivos estaticos para produccion con `collectstatic`.
- Se recomienda mover secretos y configuracion sensible a variables de entorno antes de desplegar.

---

## 12. Pruebas y validacion

Archivo principal: `dcrm/website/tests.py`

### 12.1 Cobertura funcional observada

| Area | Pruebas existentes |
|------|--------------------|
| Login | Formulario, autenticacion y persistencia de sesion |
| Roles | Admin redirige a pedidos; cliente no accede a pedidos |
| CSRF | Vista personalizada ante POST sin token valido |
| Seguridad local | Cookies seguras desactivadas en desarrollo HTTP |
| Registro | Mensajes en espanol, regex y confirmacion de contrasena |
| Clientes | Validacion de caracteres en `RecordForm` |
| Pedidos | Campos obligatorios, numero unico, regex, items y total |
| UI de pedidos | Botones para agregar/quitar productos |

### 12.2 Comandos recomendados

```powershell
cd dcrm
python manage.py check
python manage.py test website
```

### 12.3 Brechas de pruebas

Actualmente no se observan pruebas especificas para:

- Creacion de `OrderStatusHistory` mediante signals.
- Sincronizacion de `StockReservation`.
- Registro de `OrderView`.
- Eliminacion de pedidos y clientes.
- Render correcto de detalle de cliente con todos los campos actuales.

---

## 13. Instalacion y ejecucion

### 13.1 Requisitos

Opcion Docker:

- Docker
- Docker Compose

Opcion local:

- Python compatible con Django 5.2
- MySQL o MariaDB
- `pip`
- Entorno virtual recomendado

### 13.2 Ejecucion con Docker

```powershell
docker compose up -d --build
docker compose ps
```

Abrir:

```text
http://127.0.0.1:8000/
```

### 13.3 Ejecucion local

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

### 14.1 Iniciar sesion

1. Abrir `http://127.0.0.1:8000/`.
2. Si no hay sesion activa, el sistema redirige a `/login/`.
3. Ingresar usuario y contrasena.
4. Presionar **Entrar**.
5. El sistema redirige segun el rol:
   - Admin: modulo de pedidos.
   - Cliente: dashboard principal.

### 14.2 Registrar usuario

1. Abrir `/registrar/`.
2. Completar usuario, nombre, apellido, correo, contrasena y confirmacion.
3. Presionar **Registrar**.
4. Si los datos son validos, el sistema crea la cuenta e inicia sesion.
5. Los usuarios nuevos quedan como clientes normales. Para convertirlos en Admin se debe editar `is_staff` o `is_superuser` desde Django Admin.

### 14.3 Consultar dashboard de clientes

1. Iniciar sesion.
2. Abrir `/` o seleccionar **Dashboard**.
3. Revisar la tabla de clientes registrados.
4. Usar la paginacion cuando existan mas de 8 registros.
5. Presionar **Ver** para abrir el detalle de un cliente.

### 14.4 Editar cliente

1. Desde el dashboard, presionar **Ver** en un cliente.
2. Presionar **Update Record**.
3. Modificar los campos necesarios.
4. Presionar **Actualizar**.
5. El sistema valida los datos y vuelve al dashboard si la actualizacion es correcta.

### 14.5 Eliminar cliente

1. Desde el detalle del cliente, presionar **Delete**.
2. El sistema elimina el registro directamente.
3. Se muestra un mensaje de exito y se vuelve al dashboard.

Nota: en la version actual la eliminacion de clientes no tiene pantalla de confirmacion previa y se ejecuta desde un enlace GET.

---

## 15. Manual de administrador

### 15.1 Acceder al modulo de pedidos

1. Iniciar sesion con un usuario `staff` o `superuser`.
2. El sistema redirige automaticamente a `/orders/`.
3. Tambien se puede entrar desde el menu **Gestion > Listado de pedidos**.

### 15.2 Crear pedido

1. Abrir `/orders/create/` o presionar **Crear pedido**.
2. Ingresar:
   - Numero de pedido.
   - Estado del pedido.
   - Estado de pago.
3. Agregar uno o mas productos:
   - Producto.
   - Cantidad.
   - Precio unitario.
4. Usar **Agregar producto** para crear mas filas.
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
2. Revisar la pantalla de confirmacion.
3. Presionar **Si, eliminar pedido**.
4. El pedido se elimina por POST y el sistema vuelve al listado.

### 15.5 Administrar desde Django Admin

1. Crear un superusuario:

```powershell
cd dcrm
python manage.py createsuperuser
```

2. Abrir `/admin/`.
3. Iniciar sesion con el superusuario.
4. Gestionar:
   - Usuarios.
   - Records.
   - Orders.
   - OrderItems.
   - OrderStatusHistory.
   - StockReservation.
   - OrderView.

---

## 16. Resultados y valor del sistema

- Centraliza informacion de clientes y pedidos.
- Aplica roles para separar usuario cliente y administrador.
- Reduce errores de entrada con formularios validados.
- Evita edicion manual del total de pedido.
- Mantiene trazabilidad de cambios de estado.
- Permite trabajar con multiples productos por pedido.
- Usa Docker para facilitar ejecucion reproducible.
- Incluye diagramas y patrones de diseno como soporte academico/tecnico.

---

## 17. Limitaciones y hallazgos tecnicos

| Hallazgo | Impacto | Recomendacion |
|----------|---------|---------------|
| `DEBUG=True` en `settings.py` | No apto para produccion | Mover a variable de entorno |
| `SECRET_KEY` hardcodeada | Riesgo de seguridad en despliegue real | Usar variable de entorno |
| No hay ruta publica para crear `Record` | CRUD de clientes incompleto desde interfaz web | Agregar vista `create_record` si se requiere CRUD completo |
| `record.html` usa `phone` y `zipcode` | El detalle puede no mostrar telefono/codigo postal actuales | Cambiar a `phone_number` y `zip_code` |
| `update_record.html` tiene estructura HTML incompleta | Puede afectar render o estilo | Cerrar correctamente formulario/divs |
| Eliminacion de cliente por GET y sin confirmacion | Riesgo de borrado accidental o accion destructiva sin CSRF POST | Agregar pantalla de confirmacion y eliminar solo por POST |
| Pruebas sin signals/reservas/vistas | Riesgo de regresion en auditoria | Agregar pruebas para `OrderStatusHistory`, `StockReservation`, `OrderView` |
| Textos con mojibake en algunos archivos | Afecta legibilidad de UI/documentacion | Normalizar codificacion UTF-8 |
| No hay despliegue publico documentado | Entrega limitada a local/Docker | Agregar guia de despliegue |

---

## 18. Etica, privacidad y seguridad de datos

- El sistema almacena datos personales basicos de clientes: nombre, correo, telefono y direccion.
- Se recomienda limitar acceso a usuarios autorizados.
- En produccion se debe usar HTTPS.
- Se debe proteger la base de datos con credenciales robustas.
- Se recomienda establecer politicas de respaldo y retencion de datos.
- No se detecta almacenamiento de datos de tarjetas, documentos oficiales ni informacion financiera sensible.
- El proyecto no toma decisiones automatizadas con IA; por tanto no aplica evaluacion de sesgo algoritmico.

---

## 19. Checklist de entrega

- [x] Documentacion tecnica del sistema.
- [x] Manual de usuario.
- [x] Manual de administrador.
- [x] Descripcion de arquitectura.
- [x] Modelo de datos.
- [x] Rutas del sistema.
- [x] Seguridad y validaciones.
- [x] Instalacion local y Docker.
- [x] Pruebas existentes y brechas.
- [x] Limitaciones y recomendaciones.

**Repositorio:**

- GitHub: https://github.com/Braian551/AngelowDjangoOrders

**Documentos relacionados:**

- `README.md`
- `docs/patrones/patrones_diseno.md`
- `docs/arquitectura/c1.png`
- `docs/arquitectura/c2.png`
- `docs/arquitectura/c3.png`
- `docs/arquitectura/c4.png`
- `docs/Diagrama de clases.png`
