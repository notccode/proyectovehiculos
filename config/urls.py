from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración
    path('', include('vehiculo.urls')),  # Incluye las URLs de la app vehículo
]
