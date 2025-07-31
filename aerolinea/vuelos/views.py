from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto


from .serializers import (
    AvionSerializer, VueloSerializer, PasajeroSerializer,
    AsientoSerializer, ReservaSerializer, BoletoSerializer
)

class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer


class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer

    @action(detail=True, methods=['get'])
    def asientos(self, request, pk=None):
        
        #Lista asientos del avion de este vuelo
        #GET /api/vuelos/{id}/asientos/
        
        vuelo = self.get_object()
        qs = Asiento.objects.filter(avion=vuelo.avion).order_by('fila', 'columna')
        serializer = AsientoSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        
        vuelo = self.get_object()
        qs = Asiento.objects.filter(avion=vuelo.avion)
        total = qs.count()
        disponibles = qs.filter(estado=Asiento.DISPONIBLE).count()
        reservados = qs.filter(estado=Asiento.RESERVADO).count()
        ocupados = qs.filter(estado=Asiento.OCUPADO).count()
        return Response({
            "vuelo": vuelo.id,
            "avion": vuelo.avion_id,
            "total": total,
            "disponibles": disponibles,
            "reservados": reservados,
            "ocupados": ocupados,
        })


class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer


class AsientoViewSet(viewsets.ModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().select_related('vuelo', 'pasajero', 'asiento')
    serializer_class = ReservaSerializer

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        
        reserva = self.get_object()
        if reserva.estado == Reserva.CANCELADO:
            return Response({"detail": "No se puede cancelar en este estado."}, status=status.HTTP_400_BAD_REQUEST)

        reserva.estado = Reserva.CANCELADO
        reserva.save(update_fields=['estado'])
        asiento = reserva.asiento
        asiento.estado = Asiento.DISPONIBLE
        asiento.save(update_fields=['estado'])
        return Response({"detail": "Reserva cancelada con exito."})

    @action(detail=True, methods=['post'])
    def emitir_boleto(self, request, pk=None):
        reserva = self.get_object()
        if hasattr(reserva, 'boleto'):
            return Response({"detail": "La reserva ya tiene una tarjeta de embarque."}, status=status.HTTP_400_BAD_REQUEST)

        if reserva.estado == Reserva.CANCELADO:
            return Response({"detail": "No se puede emitir boleto con la reserva en este estado."}, status=status.HTTP_400_BAD_REQUEST)

        boleto = Boleto.objects.create(
            reserva=reserva,
            codigo_barra=str(reserva.codigo_reserva), 
            estado="Emitido"
        )
        return Response(BoletoSerializer(boleto).data, status=status.HTTP_201_CREATED)


class BoletoViewSet(viewsets.ModelViewSet):
    queryset = Boleto.objects.all().select_related('reserva')
    serializer_class = BoletoSerializer