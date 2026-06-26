from django.db import models


class Record(models.Model):
    """
    Modelo que guarda la información básica de cada cliente.

    Patrón de persistencia: ORM / Active Record.
    La clase representa una tabla y cada instancia representa una fila.
    """

    # Fecha y hora en que se crea el registro. Django la asigna automáticamente.
    created_at = models.DateTimeField(auto_now_add=True)

    # Datos personales y de contacto del cliente.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)

    # Dirección del cliente.
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        """Muestra el registro de forma legible en el administrador y consola."""
        return f"{self.first_name} {self.last_name} - {self.email}"
