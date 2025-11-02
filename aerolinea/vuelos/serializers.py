from rest_framework import serializers
from .models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto
from .models import Reserva



class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'



class AvionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avion
        fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):
     avion = AvionSerializer(read_only=True)

def validate(self, data):
    fecha_salida = data.get('fecha_salida') or getattr(self.instance, 'fecha_salida', None)
    fecha_llegada = data.get('fecha_llegada') or getattr(self.instance, 'fecha_llegada', None)

    if fecha_salida and fecha_llegada and fecha_llegada <= fecha_salida:
            raise serializers.ValidationError("La fecha_llegada debe ser posterior a fecha_salida.")
    return data


class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = '__all__'


class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    # opcional: mostrar info adicional de lectura
    vuelo_detalle = VueloSerializer(source='vuelo', read_only=True)
    pasajero_detalle = PasajeroSerializer(source='pasajero', read_only=True)
    asiento_detalle = AsientoSerializer(source='asiento', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'vuelo', 'vuelo_detalle', 'pasajero', 'pasajero_detalle',
            'asiento', 'asiento_detalle', 'estado', 'fecha_reserva',
            'precio', 'codigo_reserva'
        ]
        read_only_fields = ['fecha_reserva', 'codigo_reserva']

    def validate(self, data):
        # Validación: un pasajero no puede tener más de una reserva en el mismo vuelo
        vuelo = data.get('vuelo') or getattr(self.instance, 'vuelo', None)
        pasajero = data.get('pasajero') or getattr(self.instance, 'pasajero', None)
        asiento = data.get('asiento') or getattr(self.instance, 'asiento', None)

        if vuelo and pasajero:
            existe = Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero)
            if self.instance:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise serializers.ValidationError("El pasajero ya tiene una reserva para este vuelo.")

        # Validación: el asiento debe pertenecer al avión asignado al vuelo
        if vuelo and asiento:
            if asiento.avion_id != vuelo.avion_id:
                raise serializers.ValidationError("El asiento no pertenece al avión de este vuelo.")

        # Validación: el asiento debe estar disponible (según el campo estado)
        # Asumimos que 1 = DISPONIBLE en tu modelo
        if asiento and hasattr(asiento, 'estado') and asiento.estado != Asiento.DISPONIBLE:
            raise serializers.ValidationError("El asiento no está disponible.")

        return data

    def create(self, validated_data):
        # Creamos la reserva y actualizamos el estado del asiento a "Reservado"
        reserva = super().create(validated_data)
        asiento = reserva.asiento
        asiento.estado = Asiento.RESERVADO
        asiento.save(update_fields=['estado'])
        return reserva

    def update(self, instance, validated_data):
        # Si cambia el asiento, liberar el anterior y reservar el nuevo
        asiento_anterior = instance.asiento
        reserva = super().update(instance, validated_data)
        asiento_nuevo = reserva.asiento
        if asiento_anterior != asiento_nuevo:
            asiento_anterior.estado = Asiento.DISPONIBLE
            asiento_anterior.save(update_fields=['estado'])
            asiento_nuevo.estado = Asiento.RESERVADO
            asiento_nuevo.save(update_fields=['estado'])
        return reserva


class BoletoSerializer(serializers.ModelSerializer):
    reserva_detalle = ReservaSerializer(source='reserva', read_only=True)

    class Meta:
        model = Boleto
        fields = ['id', 'reserva', 'reserva_detalle', 'codigo_barra', 'fecha_emision', 'estado']
        read_only_fields = ['fecha_emision']
