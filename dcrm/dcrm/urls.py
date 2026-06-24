from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: Agregar 'include'

# Este archivo conecta las URLs globales del proyecto con la app principal.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')), # Redirige la raíz a la app 'website'
]
