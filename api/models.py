from django.db import models

# Definición del modelo Inventario
class Inventario(models.Model):
    # Nombre del producto
    name = models.CharField(max_length=50, null=False, default='noname')
    # Precio del producto
    price = models.FloatField(null=False, default=0)
    # Stock disponible del producto
    stock = models.IntegerField(null=False, default=0)
    # Categoría del producto
    category = models.CharField(max_length=150, null=False, default='nocategory')
    # Indica si el producto tiene descuento o no
    isdiscount = models.BooleanField(default=False)
    # Porcentaje de descuento aplicado al producto (si isdiscount es True)
    discount = models.IntegerField(null=True)
    # Estado del producto (puede ser 'ACTIVO' o 'INACTIVO')
    state =  models.CharField(max_length=15, null=False, default='ACTIVO')

    # Método para representar el objeto como una cadena
    def __str__(self):
        return self.name

# Definición del modelo Usuarios
class Usuarios(models.Model):
    # Nombre de usuario
    user = models.CharField(max_length=50, null=False)
    # Dirección de correo electrónico del usuario
    email= models.EmailField(max_length=200, null=False)
    # Contraseña del usuario
    password = models.CharField(max_length=50, null=False)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return self.user
