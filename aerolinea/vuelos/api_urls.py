from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_ping(request):
    return Response({"status": "ok", "message": "API funcionando correctamente"})

urlpatterns = [
    path('ping/', api_ping),
]
