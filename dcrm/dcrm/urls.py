from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: Agregar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')), # Redirige la raíz a la app 'website'
]