from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Asiento, Vuelo, Pasajero, Reserva
from vuelos.models import Avion

admin.site.register(Avion)
admin.site.register(Asiento)
admin.site.register(Vuelo)
admin.site.register(Pasajero)
admin.site.register(Reserva)
