# from django.contrib import admin
# from django.urls import path, include  
# from vuelos import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('vuelos.urls')), 
#     path('api-auth/', include('rest_framework.urls')),  
#     path('', include('vuelos.site_urls')),
#     path('accounts/', include('django.contrib.auth.urls')),
#     #path('', views.HomeView.as_view(), name='home'),
#      path("", views.HomeView, name="home"),
#     path('logout/', views.logout_view, name='logout'),
#     path("vuelos/", views.lista_vuelos, name="lista_vuelos"),
#     path("vuelos/<int:vuelo_id>/asientos/", views.seleccionar_asiento, name="seleccionar_asiento"),
#     path("vuelos/<int:vuelo_id>/asientos/<int:asiento_id>/confirmar/", views.confirmar_reserva, name="confirmar_reserva"),
#     path("reserva/<int:reserva_id>/", views.detalle_reserva, name="detalle_reserva"),

#     path("vuelo/<int:pk>/", views.detalle_reserva, name="detalle_recerva"),
#     path("", views.HomeView, name="home"),
#     path("vuelo/<int:pk>/", views.detalle_reserva, name="detalle_vuelo"),
#     path("mis-reservas/", views.MisReservasView, name="mis_reservas"),
# ]

# from django.contrib import admin
# from django.urls import path, include  
# from vuelos import views as vuelos_views 
#from vuelos import views
#from views import HomeView, ReservarView, MisReservasView, SobreNosotrosView, registro_view


#urlpatterns = [
 #   path('admin/', admin.site.urls),
  #  path('api/', include('vuelos.urls')), 
   # path('registro/', vuelos_views.registro, name='registro'),
    #path('api-auth/', include('rest_framework.urls')),  
    #path('', include('vuelos.site_urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('', views.home, name='home'), 

    # Usar .as_view() para vistas basadas en clases
    #path("", views.HomeView.as_view(), name="home"),
    #path('logout/', views.logout_view, name='logout'),
    #path("vuelos/", views.lista_vuelos, name="lista_vuelos"),
    #path("vuelos/<int:vuelo_id>/asientos/", views.seleccionar_asiento, name="seleccionar_asiento"),
    #path("reserva/<int:reserva_id>/", views.detalle_reserva, name="detalle_reserva"),

    # Elegí una sola ruta para vuelo/ y corregí el nombre de la vista
    #path("vuelo/<int:pk>/", views.detalle_reserva, name="detalle_reserva"),

    # Vista basada en clases, agregar .as_view()
    #path("mis-reservas/", views.MisReservasView.as_view(), name="mis_reservas"),

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("vuelos.urls")),  # todas las rutas de la app vuelos
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
