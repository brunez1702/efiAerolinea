from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vuelo, Avion, Asiento, Pasajero,Reserva
from .forms import RegistroForm, ReservaForm
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework import viewsets, permissions
from .serializers import VueloSerializer, AvionSerializer, AsientoSerializer, PasajeroSerializer, ReservaSerializer
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



class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class RegistroView(FormView):
    template_name = "registro.html"
    form_class = RegistroForm
    success_url = "/login/" 

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Cuenta creada. Inicia sesión.")
        return super().form_valid(form)


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")



class ReservaView(LoginRequiredMixin, FormView):
    template_name = "reservar.html"
    form_class = ReservaForm
    success_url = "/mis_reservas/"

    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.usuario = self.request.user
        reserva.save()
        messages.success(self.request, "Reserva realizada con éxito.")
        return super().form_valid(form)



class MisReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "mis_reservas.html"
    context_object_name = "reservas"

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

class SobreNosotrosView(View):    
    def sobre_nosotros(request):
        return render(request, "sobre_nosotros.html")
