from django.urls import path
from .views import HomeView, ReservarView, MisReservasView, SobreNosotrosView, registro_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reservar/', ReservarView.as_view(), name='reservar'),
    path('mis-reservas/', MisReservasView.as_view(), name='mis_reservas'),
    path('sobre-nosotros/', SobreNosotrosView.as_view(), name='sobre_nosotros'),
    path('registro/', registro_view, name='registro'),
]
