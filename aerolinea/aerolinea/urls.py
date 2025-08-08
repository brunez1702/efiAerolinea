from django.contrib import admin
from django.urls import path, include  
from vuelos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vuelos.urls')), 
    path('api-auth/', include('rest_framework.urls')),  
    path('', include('vuelos.site_urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('logout/', views.logout_view, name='logout'),
    path("vuelos/", views.lista_vuelos, name="lista_vuelos"),
    path("vuelos/<int:vuelo_id>/asientos/", views.seleccionar_asiento, name="seleccionar_asiento"),
    path("vuelos/<int:vuelo_id>/asientos/<int:asiento_id>/confirmar/", views.confirmar_reserva, name="confirmar_reserva"),
    path("reserva/<int:reserva_id>/", views.detalle_reserva, name="detalle_reserva"),
]
