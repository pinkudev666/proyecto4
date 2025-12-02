# temucosoft_backend/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperAdminOrAdminCliente(BasePermission):
    """
    Permite acceso si el request.user es super_admin o admin_cliente.
    Si es admin_cliente, la creación se limitará en la vista/serializer.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ('super_admin', 'admin_cliente')

class IsSelfOrSuperAdmin(BasePermission):
    """
    Permite GET si el usuario pide su propio recurso (pk == request.user.pk)
    o si es super_admin (puede ver cualquier usuario).
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'super_admin':
            return True
        return obj.pk == request.user.pk