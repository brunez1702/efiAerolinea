from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from .views import AvionViewSet, AsientoViewSet, VueloViewSet, PasajeroViewSet, ReservaViewSet

# --- Router principal ---
router = DefaultRouter()
router.register(r'aviones', AvionViewSet)
router.register(r'asientos', AsientoViewSet)
router.register(r'vuelos', VueloViewSet)
router.register(r'pasajeros', PasajeroViewSet)
router.register(r'reservas', ReservaViewSet, basename='reserva')

# --- Swagger / Redoc ---
schema_view = get_schema_view(
    openapi.Info(
        title="API Aerolinea",
        default_version='v1',
        description="Documentación de la API",
        contact=openapi.Contact(email="tu_email@dominio.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# --- URLs ---
urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("reservar/", views.reservar, name="reservar"),
    path("mis-reservas/", views.mis_reservas, name="mis_reservas"),
    path("sobre-nosotros/", views.sobre_nosotros, name="sobre_nosotros"),

    # Admin y API
    #path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger / Redoc
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
