from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite solo a administradores hacer acciones de escritura.
    Otros usuarios solo pueden leer (GET).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user.is_authenticated and request.user.rol == 'admin'
        return obj.usuario == request.user or request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite que solo el propietario (pasajero) o admin pueda modificar/ver su propia reserva.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.rol == 'admin':
            return True
        return obj.pasajero.user == request.user  # Asumiendo que Pasajero tiene relación con Usuario
