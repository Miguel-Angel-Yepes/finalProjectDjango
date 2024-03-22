from django.urls import path
from . import views

# Definición de las URLs para las vistas
urlpatterns = [
    path('agregar/', views.agregar, name='agregar'),  # URL para la vista de agregar un producto al inventario
    path('gestion/', views.gestion, name='gestion'),  # URL para la vista de gestión del inventario
    path('actualizar/<int:producto_id>/', views.actualizar, name='actualizar'),  # URL para la vista de actualizar un producto específico en el inventario
    path('detalles_producto/<int:producto_id>/', views.detalles_producto, name='detalles_producto'),  # URL para la vista de ver los detalles de un producto en el inventario
    path('eliminar/<int:producto_id>/', views.eliminar, name='eliminar'),  # URL para la vista de eliminar un producto del inventario
    path('login/', views.login, name='login'),  # URL para la vista de inicio de sesión
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),  # URL para la vista de crear una nueva cuenta de usuario
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),  # URL para la vista de cerrar sesión
]
