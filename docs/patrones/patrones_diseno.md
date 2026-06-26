# Patrones de diseno documentados

Este documento registra 10 patrones usados en AngeloDjangoOrders. No todos son patrones GoF puros: el proyecto combina patrones del catalogo GoF con patrones arquitectonicos y convenciones propias de Django.

## Diagramas UML incluidos

Se entregan 4 diagramas PlantUML de patrones elegidos:

- [Observer](observer.puml): signals de Django reaccionan ante cambios de `Order`.
- [Decorator](decorator.puml): decoradores protegen vistas con autenticacion, autorizacion, CSRF y cache.
- [State](state.puml): `Order` y `StockReservation` representan fases mediante campos `choices`.
- [ModelForm / Form Object](modelform_form_object.puml): formularios Django validan datos antes de guardar modelos.

## 1. Observer

- Tipo: GoF de comportamiento.
- Ubicacion: `dcrm/website/signals.py`, `dcrm/website/apps.py`.
- Participantes: `Order`, `capture_previous_order_state()`, `create_order_status_history()`, `OrderStatusHistory`.
- Como se usa: Django emite eventos `pre_save` y `post_save` cuando se guarda un pedido. Las funciones receptoras escuchan esos eventos y crean historial sin que cada vista tenga que repetir esa logica.
- Beneficio: reduce acoplamiento entre vistas y auditoria de pedidos.

## 2. Decorator

- Tipo: GoF estructural, aplicado mediante decoradores de Python/Django.
- Ubicacion: `dcrm/website/views/order_views.py`.
- Participantes: `login_required`, `user_passes_test(is_admin_user)`, `ensure_csrf_cookie`, `never_cache`, vistas de pedidos.
- Como se usa: las funciones de vista se envuelven con decoradores que agregan autenticacion, autorizacion, proteccion CSRF y control de cache sin modificar el cuerpo principal de cada vista.
- Beneficio: separa reglas transversales de seguridad del flujo propio de crear, editar, listar o eliminar pedidos.

## 3. State

- Tipo: GoF de comportamiento aplicado de forma simple.
- Ubicacion: `dcrm/website/models/order.py`.
- Participantes: `Order.status`, `Order.payment_status`, `StockReservation.status`, metodos `change_status()`, `reserve()`, `expire()` y `release()`.
- Como se usa: los estados se representan con constantes y `choices` de Django. No hay clases de estado separadas; por eso es una implementacion ligera inspirada en State, no una version GoF completa.
- Beneficio: limita las fases permitidas de pedidos, pagos y reservas.

## 4. Factory Method

- Tipo: GoF creacional aplicado mediante factory helper de Django.
- Ubicacion: `dcrm/website/forms/order_form.py`.
- Participantes: `inlineformset_factory`, `OrderItemFormSet`, `Order`, `OrderItem`, `OrderItemForm`.
- Como se usa: `inlineformset_factory()` crea una clase de formset configurada para editar varios `OrderItem` asociados a un `Order`.
- Beneficio: evita construir manualmente la clase que administra formularios hijos y mantiene la configuracion en un unico punto.

## 5. Strategy

- Tipo: GoF de comportamiento usado de forma sencilla.
- Ubicacion: `dcrm/website/views/helpers.py`, `dcrm/website/views/auth_views.py`, `dcrm/website/views/order_views.py`.
- Participantes: `is_admin_user()`, `get_login_redirect_url()`, `user_passes_test()`.
- Como se usa: funciones separadas encapsulan reglas intercambiables de autorizacion y redireccion. Por ejemplo, `user_passes_test()` recibe la regla `is_admin_user` como criterio para permitir o bloquear acceso.
- Beneficio: permite cambiar la politica de acceso o redireccion sin reescribir las vistas.

## 6. Facade

- Tipo: patron estructural, aplicado como fachada de flujo.
- Ubicacion: `dcrm/website/views/order_views.py`.
- Participantes: `create_order()`, `update_order()`, `delete_order()`, `sync_stock_reservations()`, `record_order_view()`.
- Como se usa: las vistas de pedidos exponen operaciones simples al usuario y coordinan internamente formularios, modelos, mensajes, reservas, totales y plantillas.
- Beneficio: oculta detalles de persistencia y sincronizacion detras de acciones de alto nivel.

## 7. Template Method

- Tipo: GoF de comportamiento aplicado por el framework Django.
- Ubicacion: `dcrm/website/forms/order_form.py`, `dcrm/website/forms/signup_form.py`, `dcrm/website/forms/record_form.py`.
- Participantes: `is_valid()`, `clean()`, `clean_order_number()`, `clean_quantity()`, `clean_unit_price()`, `clean_password1()`, `clean_password2()`.
- Como se usa: Django define el flujo general de validacion del formulario y el proyecto personaliza pasos concretos mediante metodos `clean_*` y `clean()`.
- Beneficio: permite extender la validacion sin reemplazar todo el algoritmo interno de Django Forms.

## 8. MTV

- Tipo: patron arquitectonico de Django, no GoF.
- Ubicacion: `dcrm/website/models/`, `dcrm/website/views/`, `dcrm/website/templates/`.
- Participantes: modelos `Order`, `OrderItem`, `Record`; vistas de `auth_views.py`, `record_views.py`, `order_views.py`; plantillas HTML.
- Como se usa: el Modelo concentra datos y reglas de dominio, la Vista coordina peticiones y respuestas, y el Template renderiza la interfaz HTML.
- Beneficio: separa responsabilidades y evita mezclar SQL, flujo HTTP y presentacion.

## 9. ORM / Active Record

- Tipo: patron de persistencia y convencion Django, no GoF.
- Ubicacion: `dcrm/website/models/order.py`, `dcrm/website/models/record.py`.
- Participantes: clases que heredan de `models.Model`, managers como `Order.objects`, metodos de dominio como `calculate_total()`.
- Como se usa: cada modelo representa una tabla y tambien ofrece metodos para consultar, guardar, actualizar y ejecutar logica cercana al dato.
- Beneficio: permite trabajar con objetos Python en lugar de SQL directo y mantiene parte de la logica de negocio junto a los datos.

## 10. ModelForm / Form Object

- Tipo: patron/convenio de Django, no GoF.
- Ubicacion: `dcrm/website/forms/`.
- Participantes: `OrderForm`, `OrderItemForm`, `RecordForm`, `SignUpForm`.
- Como se usa: los formularios encapsulan entrada de usuario, widgets, etiquetas, mensajes de error y validaciones antes de crear o modificar modelos.
- Beneficio: evita que las vistas acumulen validaciones y hace reutilizable la logica de entrada.


