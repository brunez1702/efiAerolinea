from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vuelos.urls')), 
    path('api-auth/', include('rest_framework.urls')),  
    path('', include('vuelos.site_urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
