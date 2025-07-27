from django.db import models
from django.contrib.auth.models import AbstractUser # para contrase;as
import uuid 


#1 avion
class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    filas = models.IntegerField()
    columnas = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} ({self.capacidad} asientos)"


#2 vuelo
class Vuelo(models.Model):
    PROGRAMADO = 1
    DEMORADO = 2
    CANCELADO = 3
    FINALIZADO = 4

    ESTADOS = [
        (PROGRAMADO, 'Programado'),
        (DEMORADO, 'Demorado'),        
        (CANCELADO, 'Cancelado'),
        (FINALIZADO, 'Finalizado'),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    estado = models.IntegerField(choices=ESTADOS, default=PROGRAMADO)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vuelo {self.id} - {self.origen} → {self.destino}"


#3 pasajero
class Pasajero(models.Model):
    DNI = 1
    PASAPORTE = 2
    OTRO = 3

    TIPO_DOC = [
        (DNI, 'DNI'),
        (PASAPORTE, 'Pasaporte'),
        (OTRO, 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    tipo_documento = models.IntegerField(choices=TIPO_DOC, default=DNI)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.documento})"


#5 asiento - lo tengo que poner arriba de reserva porque lo necesito para la reserva
class Asiento(models.Model):
    DISPONIBLE = 1
    RESERVADO = 2
    OCUPADO = 3

    ESTADO = [
        (DISPONIBLE, 'Disponible'),
        (RESERVADO, 'Reservado'),
        (OCUPADO, 'Ocupado'),
    ]
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=5)
    fila = models.IntegerField()
    columna = models.CharField(max_length=1)
    tipo = models.CharField(max_length=20, blank=True)
    estado = models.IntegerField(choices=ESTADO, default=DISPONIBLE)

    def __str__(self):
        return f"Asiento {self.numero} ({self.estado})"


#4 reserva
class Reserva(models.Model):
    RESERVADO = 1
    CANCELADO = 2
    OCUPADO = 3

    ESTADO = [
        (RESERVADO, 'Reservado'),
        (CANCELADO, 'Cancelado'),
        (OCUPADO, 'Ocupado'),
    ]

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    asiento = models.OneToOneField(Asiento, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO, default=RESERVADO)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_reserva = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Reserva {self.codigo_reserva}"


# 6 usuario
class Usuario(models.Model):
    ADMINISTRADOR = 1
    CLIENTE = 2

    ROL = [
        (ADMINISTRADOR, 'Administrador'),
        (CLIENTE, 'Cliente'),
    ]

    nombre_usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=100)
    rol = models.IntegerField(choices=ROL, default=CLIENTE)

    def __str__(self):
        return f"{self.email}"

#7 boletp
class Boleto(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    codigo_barra = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="Emitido")

    def __str__(self):
        return f"Boleto {self.id} - {self.reserva}"
