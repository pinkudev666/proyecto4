from rest_framework import serializers
from .models import User, Product, Branch, Inventory, Supplier, Sale, Purchase, Company
from django.contrib.auth import get_user_model

# -----------------------------
# SERIALIZADOR USER
# -----------------------------
User = get_user_model()
Company = User._meta.get_field('company').related_model  # referencia dinámica al modelo Company

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'rut', 'company', 'is_active', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'required': False},
            'rut': {'required': False, 'allow_null': True},
        }

    def validate_role(self, value):
        # validar que el rol exista entre los choices del modelo
        allowed = {r for r, _ in User.ROLE_CHOICES}
        if value not in allowed:
            raise serializers.ValidationError("Rol inválido.")
        # prevenimos crear super_admin desde este endpoint
        if value == 'super_admin':
            raise serializers.ValidationError("No está permitido crear super_admin desde este endpoint.")
        return value

    def validate(self, data):
        """
        Validación cross-field:
        - admin_cliente, gerente, vendedor => requieren company
        - cliente_final => company opcional
        """
        role = data.get('role')
        company = data.get('company', None)

        if role in ['admin_cliente', 'gerente', 'vendedor'] and not company:
            raise serializers.ValidationError({'company': f"Usuarios con rol '{role}' deben tener una company asignada."})

        return data

    def create(self, validated_data):
        """
        Usamos create_user (si lo tienes definido) o fallback a crear con set_password.
        create_user normalmente toma username, email, password y otros kwargs.
        """
        password = validated_data.pop('password')
        # Si tu UserManager implementa create_user aceptando role, rut, company e is_active, úsalo:
        try:
            user = User.objects.create_user(password=password, **validated_data)
        except TypeError:
            # fallback si create_user tiene distinta firma: construir manualmente
            user = User(**validated_data)
            user.set_password(password)
            user.save()
        return user

# -----------------------------
# SERIALIZADOR COMPANY
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'rut', 'created_at']


# -----------------------------
# SERIALIZADOR PRODUCT
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# -----------------------------
# SERIALIZADOR BRANCH
# -----------------------------
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

# -----------------------------
# SERIALIZADOR INVENTORY
# -----------------------------
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

# -----------------------------
# SERIALIZADOR SUPPLIER
# -----------------------------
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# -----------------------------
# SERIALIZADOR SALE
# -----------------------------
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

# -----------------------------
# SERIALIZADOR PURCHASE
# -----------------------------
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
