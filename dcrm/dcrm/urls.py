from django.contrib import admin
from django.urls import include, path

# Este archivo conecta las URLs globales del proyecto con la app principal.
urlpatterns = [
    # Panel administrativo generado por Django Admin.
    path('admin/', admin.site.urls),

    # La raíz del sitio se delega a `website.urls`.
    path('', include('website.urls')),
]
