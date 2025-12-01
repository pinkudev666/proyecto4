from rest_framework import serializers
from .models import User, Product, Branch, Inventory, Supplier, Sale, Purchase, Company

# -----------------------------
# SERIALIZADOR USER
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'rut', 'company']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            rut=validated_data['rut'],
            company=validated_data['company'],
            is_active=validated_data.get('is_active', True)
        )
        user.set_password(validated_data['password'])
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
