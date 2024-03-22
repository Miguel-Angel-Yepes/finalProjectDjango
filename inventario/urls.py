"""
Configuración de URL para el proyecto inventario.

La lista `urlpatterns` enruta las URL a vistas. Para obtener más información, consulte:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Ejemplos:
Vistas basadas en funciones
    1. Agregar una importación:  from my_app import views
    2. Agregar una URL a urlpatterns:  path('', views.home, name='home')
Vistas basadas en clases
    1. Agregar una importación:  from other_app.views import Home
    2. Agregar una URL a urlpatterns:  path('', Home.as_view(), name='home')
Inclusión de otro URLconf
    1. Importar la función include(): from django.urls import include, path
    2. Agregar una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

# Definición de las URLs para el proyecto
urlpatterns = [
    path('admin/', admin.site.urls),  # URL para acceder a la interfaz de administración de Django
    path('', views.home, name='home'),  # URL para la vista de inicio del proyecto
    path('Api/', include('api.urls')),  # URL para incluir las URLs del módulo 'api'
]
