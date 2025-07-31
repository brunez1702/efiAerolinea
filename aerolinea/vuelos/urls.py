from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AvionViewSet, VueloViewSet, PasajeroViewSet,
    AsientoViewSet, ReservaViewSet, BoletoViewSet
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
]