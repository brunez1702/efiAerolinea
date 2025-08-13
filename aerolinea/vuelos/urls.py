from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    AvionViewSet, VueloViewSet, PasajeroViewSet,
    AsientoViewSet, ReservaViewSet, BoletoViewSet, 
    MiLoginView
)


router = DefaultRouter()
router.register(r'aviones', AvionViewSet)
router.register(r'vuelos', VueloViewSet)
router.register(r'pasajeros', PasajeroViewSet)
router.register(r'asientos', AsientoViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'boletos', BoletoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MiLoginView.as_view(), name='login'),

    path('confirmar/<str:codigo_reserva>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('descargar-boleto/<int:reserva_id>/', views.descargar_boleto, name='descargar_boleto'),
]