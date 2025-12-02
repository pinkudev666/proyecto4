from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_superuser', 'company')
    list_filter = ('role', 'is_superuser', 'company')
    fieldsets = (
        (None, {'fields': ('username','password')}),
        (_('Personal info'), {'fields': ('first_name','last_name','email','rut')}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('Business'), {'fields': ('role','company')}),
        (_('Important dates'), {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1','password2','role','company'),
        }),
    )
    search_fields = ('username','email')
    ordering = ('id',)
