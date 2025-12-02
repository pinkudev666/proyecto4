from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import User, Product, Branch, Inventory, Supplier, Sale, Purchase, Company
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .serializers import (
    UserSerializer, ProductSerializer, BranchSerializer,
    InventorySerializer, SupplierSerializer, SaleSerializer,
    PurchaseSerializer, CompanySerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import PermissionDenied

# -----------------------------
# VIEWSETS
# -----------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]  # luego puedes ajustar a super_admin

# -----------------------------
# UserViewSet (con reglas)
# -----------------------------
# VIEWSETS
# -----------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]  # ajustar a super_admin si se desea

# -----------------------------
# UserViewSet (con reglas y endpoint /me/)
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    Comportamiento:
    - create: solo super_admin o admin_cliente pueden crear.
        * super_admin (o is_superuser) puede crear cualquier rol (serializer evita super_admin creation si lo deseas).
        * admin_cliente solo puede crear gerente/vendedor/cliente_final y los fuerza a su company.
    - list: super_admin lista todo, admin_cliente lista usuarios de su company, otros no pueden listar.
    - retrieve/update/destroy: super_admin (o is_superuser): acceso total;
      admin_cliente: solo usuarios de su company; gerente/vendedor: solo a sí mismos.
    - me: GET /api/users/me/ -> info del usuario autenticado
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Requerimos autenticación para todas las acciones; la lógica fina está en los métodos.
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        creator = request.user
        if not creator or not creator.is_authenticated:
            raise PermissionDenied("Debes estar autenticado para crear usuarios.")

        rol_creador = getattr(creator, "role", "") or ""
        data = request.data.copy()
        rol_nuevo = data.get("role")

        # super_admin (o is_superuser) puede crear
        if getattr(creator, "is_superuser", False) or rol_creador == "super_admin":
            return super().create(request, *args, **kwargs)

        # admin_cliente: reglas específicas
        if rol_creador == "admin_cliente":
            # prohibir creación de super_admin o admin_cliente
            if rol_nuevo in ["super_admin", "admin_cliente"]:
                raise PermissionDenied("Los admin_cliente no pueden crear usuarios de ese tipo.")
            # validar serializer y forzar company del creador
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(company=creator.company)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # otros roles no pueden crear
        raise PermissionDenied("No tienes permisos para crear usuarios.")

    def list(self, request, *args, **kwargs):
        yo = request.user
        if getattr(yo, "is_superuser", False) or (getattr(yo, "role", None) == "super_admin"):
            return super().list(request, *args, **kwargs)

        if getattr(yo, "role", None) == "admin_cliente":
            qs = self.get_queryset().filter(company_id=yo.company_id)
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)

        raise PermissionDenied("No tienes permisos para listar usuarios.")

    def get_object(self):
        """
        Reglas por objeto (retrieve/update/destroy).
        """
        obj = super().get_object()
        yo = self.request.user

        if getattr(yo, "is_superuser", False) or (getattr(yo, "role", None) == "super_admin"):
            return obj

        if getattr(yo, "role", None) == "admin_cliente":
            if obj.company_id != yo.company_id:
                raise PermissionDenied("Ese usuario no pertenece a tu empresa.")
            return obj

        if getattr(yo, "role", None) in ["gerente", "vendedor"]:
            if obj.id != yo.id:
                raise PermissionDenied("No puedes acceder a otros usuarios.")
            return obj

        raise PermissionDenied("No tienes permisos para esto.")

    # -------------------------
    # Endpoint adicional: /api/users/me/
    # -------------------------
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Devuelve los datos del usuario autenticado.
        GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
