from django.contrib import admin

from .models import Record


# Registra el modelo Record para administrarlo desde el panel de Django.
admin.site.register(Record)
