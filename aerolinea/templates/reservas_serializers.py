from rest_framework import serializers
from .models import Reserva
from vuelos.serializers import VueloSerializer, AsientoSerializer, PasajeroSerializer

class ReservaSerializer(serializers.ModelSerializer):
    vuelo = VueloSerializer(read_only=True)
    asiento = AsientoSerializer(read_only=True)
    pasajero = PasajeroSerializer(read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
