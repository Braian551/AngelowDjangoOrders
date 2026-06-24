from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Configuración principal de la app website."""

    # Django usa BigAutoField como llave primaria automática para modelos nuevos.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        """
        Carga las señales de la app cuando Django inicia.

        Esto permite que signals.py escuche eventos como:
        - antes de guardar un pedido
        - después de guardar un pedido
        """
        # Importar aquí evita cargar señales antes de que Django termine de preparar la app.
        import website.signals
