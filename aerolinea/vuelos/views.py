from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

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


class HomeView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = [
            {"titulo": "Clientes contentos", "valor": 12500},
            {"titulo": "Km recorridos", "valor": 4200000},
            {"titulo": "Flota de aviones", "valor": 18},
            {"titulo": "Vuelos completados", "valor": 32400},
        ]
        ctx["stats_descripcion"] = "Estadísticas internas estimadas por el equipo de desarrollo."
        return ctx

class ReservarView(LoginRequiredMixin, TemplateView):
    template_name = "lista_vuelos.html"

class MisReservasView(LoginRequiredMixin, TemplateView):
    template_name = "mis_reservas.html"

class SobreNosotrosView(TemplateView):
    template_name = "sobre_nosotros.html"

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
        return render(request, 'registro.html', {'form': form})
    

class MiLoginView(LoginView):
    template_name = 'login.html'  # donde vos tenés tu template

def logout_view(request):
    logout(request)  # Cierra la sesión
    return redirect('home')

def lista_vuelos(request):
    vuelos = Vuelo.objects.filter(estado=Vuelo.PROGRAMADO)
    return render(request, "reservas/lista_vuelos.html", {"vuelos": vuelos})

def seleccionar_asiento(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos = Asiento.objects.filter(avion=vuelo.avion, estado=Asiento.DISPONIBLE)
    return render(request, "reservas/seleccionar_asiento.html", {
        "vuelo": vuelo,
        "asientos": asientos
    })


def confirmar_reserva(request, vuelo_id, numero_asiento):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asiento = get_object_or_404(Asiento, vuelo=vuelo, numero=numero_asiento)
    
    if request.method == "POST":
        # Obtener datos del pasajero desde el formulario
        documento = request.POST.get("documento")
        nombre = request.POST.get("nombre")
        tipo_documento = request.POST.get("tipo_documento")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")

        pasajero, creado = Pasajero.objects.get_or_create(
            documento=documento,
            defaults={
                "nombre": nombre,
                "tipo_documento": tipo_documento,
                "email": email,
                "telefono": telefono,
                "fecha_nacimiento": fecha_nacimiento
            }
        )

        # Crear reserva
        reserva = Reserva.objects.create(
            vuelo=vuelo,
            pasajero=pasajero,
            asiento=asiento,
            precio=vuelo.precio_base
        )

        # Cambiar estado del asiento
        asiento.estado = Asiento.RESERVADO
        asiento.save()

        messages.success(request, f"Reserva confirmada. Código: {reserva.codigo_reserva}")
        return redirect("detalle_reserva", reserva_id=reserva.id)

    return render(request, "reservas/confirmar_reserva.html", {
        "vuelo": vuelo,
        "asiento": asiento
    })


def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, "reservas/detalle_reserva.html", {"reserva": reserva})


#NUEVOO
#
#
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
import qrcode
from .models import Reserva

@login_required
def confirmar_reserva(request, codigo_reserva):
    reserva = get_object_or_404(Reserva, codigo_reserva=codigo_reserva, pasajero=request.user)
    return render(request, "confirmar_reserva.html", {"reserva": reserva})

@login_required
def descargar_boleto(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, pasajero=request.user)

    # URL que irá en el QR
    url_confirmacion = request.build_absolute_uri(
        reverse('confirmar_reserva', args=[reserva.codigo_reserva])
    )

    # Generar QR con enlace
    qr = qrcode.make(url_confirmacion)

