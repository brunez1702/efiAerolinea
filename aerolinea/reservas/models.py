from django.db import models
from django.core.exceptions import ValidationError
from vuelos.models import Vuelo, Asiento, Pasajero

class Reserva(models.Model):
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name="reservas")
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name="reservas")
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name="reservas")
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vuelo", "asiento"],
                name="unique_reserva_vuelo_asiento"
            ),
            models.UniqueConstraint(
                fields=["vuelo", "asiento", "pasajero"],
                name="unique_reserva_vuelo_asiento_pasajero"
            )
        ]

    def clean(self):
        if self.asiento.avion != self.vuelo.avion:
            raise ValidationError("El asiento no pertenece a este vuelo.")

        if Reserva.objects.filter(vuelo=self.vuelo, asiento=self.asiento).exclude(pk=self.pk).exists():
            raise ValidationError("Este asiento ya está reservado en este vuelo.")

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.pasajero} - Vuelo {self.vuelo.codigo_vuelo} - Asiento {self.asiento.numero}"

