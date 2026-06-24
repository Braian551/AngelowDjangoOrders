from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        """
        Carga las señales de la app cuando Django inicia.

        Esto permite que signals.py escuche eventos como:
        - antes de guardar un pedido
        - después de guardar un pedido
        """
        import website.signals