from django.db import models
from django.contrib.auth.models import AbstractUser

class Vehiculo(models.Model):
    MARCAS = [
        ('Fiat', 'Fiat'),
        ('Chevrolet', 'Chevrolet'),
        ('Ford', 'Ford'),
        ('Toyota', 'Toyota'),
    ]
    
    CATEGORIAS = [
        ('Particular', 'Particular'),
        ('Transporte', 'Transporte'),
        ('Carga', 'Carga'),
    ]
    
    marca = models.CharField( max_length=20, choices=MARCAS, default='Ford',)
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50, unique=True) 
    serial_motor = models.CharField(max_length=50, unique=True) 
    categoria = models.CharField( max_length=20, choices=CATEGORIAS, default='Particular',)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.marca} {self.modelo}'
    
    class Meta:
        permissions = [
        ("visualizar_catalogo", "Puede visualizar catálogo de Vehículos"),
        ("add_vehiculomodel", "Can add Vehiculo model"),
        ]


class User(AbstractUser):
    role = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
