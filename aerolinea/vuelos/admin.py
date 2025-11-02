from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Vuelo, Reserva

@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ['codigo_vuelo', 'origen', 'destino', 'fecha_salida', 'precio', 'asientos_disponibles']
    list_filter = ['origen', 'destino', 'fecha_salida']
    search_fields = ['codigo_vuelo', 'origen', 'destino']
    ordering = ['fecha_salida']
    list_per_page = 20
    
    fieldsets = (
        ('Información del Vuelo', {
            'fields': ('codigo_vuelo', 'origen', 'destino')
        }),
        ('Horarios', {
            'fields': ('fecha_salida', 'fecha_llegada')
        }),
        ('Detalles Comerciales', {
            'fields': ('precio', 'asientos_disponibles')
        }),
    )

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['codigo_reserva', 'usuario', 'vuelo', 'numero_pasajeros', 'fecha_reserva', 'total_precio']
    list_filter = ['fecha_reserva', 'vuelo__origen', 'vuelo__destino']
    search_fields = ['codigo_reserva', 'usuario__username', 'vuelo__codigo_vuelo']
    ordering = ['-fecha_reserva']
    list_per_page = 20
    readonly_fields = ['codigo_reserva', 'fecha_reserva', 'total_precio']
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('codigo_reserva', 'usuario', 'vuelo')
        }),
        ('Detalles', {
            'fields': ('numero_pasajeros', 'fecha_reserva')
        }),
        ('Total', {
            'fields': ('total_precio',)
        }),
    )
    
    def total_precio(self, obj):
        return f"${obj.total_precio()}"
    total_precio.short_description = "Total a Pagar"
