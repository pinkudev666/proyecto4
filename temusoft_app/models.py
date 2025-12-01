from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=200)
    rut = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin','Super Admin'),
        ('admin_cliente','Admin Cliente'),
        ('gerente','Gerente'),
        ('vendedor','Vendedor'),
        ('cliente_final','Cliente Final'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    rut = models.CharField(max_length=12, blank=True, null=True)
    company = models.ForeignKey(
        Company,
        null=True,  # super_admin puede no tener company
        blank=True,
        on_delete=models.PROTECT,
        related_name='users'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        #mValidaciones según el rol del usuario
        if self.role == 'super_admin' and self.company is not None:
            raise ValidationError("Super admin no puede tener company.")
        if self.role in ['admin_cliente', 'gerente', 'vendedor'] and not self.company:
            raise ValidationError(f"Usuarios con rol {self.role} deben tener una company asignada.")

    def save(self, *args, **kwargs):
        # Llamamos a la validación antes de guardar
        self.clean()
        # Si es super_admin, aseguramos company=None
        if self.role == 'super_admin':
            self.company = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Subscription(models.Model):
    PLAN_CHOICES = (('basico','Básico'),('estandar','Estándar'),('premium','Premium'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=30, blank=True)

class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=200)
    rut = models.CharField(max_length=12)
    contact = models.CharField(max_length=200, blank=True)

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)

class Purchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    items = models.JSONField()  # para rapidez: list of {sku, qty, price}

class Sale(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    items = models.JSONField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

