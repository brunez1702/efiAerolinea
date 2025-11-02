from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reserva
from .forms import RegistroForm, ReservaForm

from rest_framework import viewsets, permissions
from .models import Vuelo, Avion, Asiento, Pasajero
from .serializers import VueloSerializer, AvionSerializer, AsientoSerializer, PasajeroSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo admin puede crear/editar/eliminar

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsOwnerOrAdmin] 
# 🔹 ViewSet de Aviones
class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 🔹 ViewSet de Asientos
class AsientoViewSet(viewsets.ModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 🔹 ViewSet de Vuelos
class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 🔹 ViewSet de Pasajeros
class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



def home(request):
    return render(request, "home.html")

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente. Inicia sesión.")
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})

def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def cerrar_sesion(request):
    logout(request)
    return redirect("home")

@login_required
def reservar(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("mis_reservas")
    else:
        form = ReservaForm()
    return render(request, "reservar.html", {"form": form})

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, "mis_reservas.html", {"reservas": reservas})

def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")
