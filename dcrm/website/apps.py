from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Configuración principal de la aplicación website."""

    # Define el tipo de campo automático para las llaves primarias creadas por Django.
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación dentro del proyecto.
    name = 'website'
