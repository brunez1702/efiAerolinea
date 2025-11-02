from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Reserva
from .models import Vuelo, Avion, Asiento, Pasajero
from .serializers import VueloSerializer, AvionSerializer, AsientoSerializer, PasajeroSerializer, ReservaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOrAdmin


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reserva.objects.all()


    def perform_create(self, serializer):
        serializer.save(pasajero=self.request.user)

    @action(detail=False, methods=['get'])
    def mis_reservas(self, request):
        reservas = Reserva.objects.filter(pasajero=request.user)
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)

class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer

class AsientoViewSet(viewsets.ModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer

class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
