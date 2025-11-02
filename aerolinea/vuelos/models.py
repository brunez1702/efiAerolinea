from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.conf import settings

# 1️⃣ Avión

class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    filas = models.IntegerField()
    columnas = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} ({self.capacidad} asientos)"

# 2️⃣ Vuelo

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

    codigo_vuelo = models.CharField(max_length=10, unique=True)
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField(blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=PROGRAMADO)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    asientos_disponibles = models.IntegerField(default=180)

    def save(self, *args, **kwargs):
        if not self.duracion:
            self.duracion = self.fecha_llegada - self.fecha_salida
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_vuelo} - {self.origen} → {self.destino}"

    class Meta:
        ordering = ['fecha_salida']

# 3️⃣ Pasajero

class Pasajero(models.Model):
    DNI = 1
    PASAPORTE = 2
    OTRO = 3

    TIPO_DOC = [
        (DNI, 'DNI'),
        (PASAPORTE, 'Pasaporte'),
        (OTRO, 'Otro'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    tipo_documento = models.IntegerField(choices=TIPO_DOC, default=DNI)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

# 4️⃣ Asiento

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
        return f"Asiento {self.numero} ({self.get_estado_display()})"

# 5️⃣ Reserva

class Reserva(models.Model):
    RESERVADO = 1
    CANCELADO = 2
    OCUPADO = 3

    ESTADO = [
        (RESERVADO, 'Reservado'),
        (CANCELADO, 'Cancelado'),
        (OCUPADO, 'Ocupado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, null=True, blank=True)
    asiento = models.OneToOneField(Asiento, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.IntegerField(choices=ESTADO, default=RESERVADO)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    codigo_reserva = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vuelo', 'pasajero'], name='unico_pasajero_por_vuelo'),
        ]
        ordering = ['-fecha_reserva']

    def save(self, *args, **kwargs):
        if not self.precio:
            self.precio = self.vuelo.precio_base
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.codigo_reserva}"

# 6️⃣ Usuario (extra, opcional)

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

# 7️⃣ Boleto

class Boleto(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    codigo_barra = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="Emitido")

    def __str__(self):
        return f"Boleto {self.id} - {self.reserva.codigo_reserva}"
