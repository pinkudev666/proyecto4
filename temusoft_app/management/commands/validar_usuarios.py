from django.core.management.base import BaseCommand
from temusoft_app.models import User  # reemplaza 'myapp' por tu app

class Command(BaseCommand):
    help = 'Valida usuarios según roles y company'

    def handle(self, *args, **kwargs):
        # Script de validación
        usuarios_sin_company = User.objects.filter(
            role__in=['admin_cliente', 'gerente', 'vendedor'],
            company__isnull=True
        )
        if usuarios_sin_company.exists():
            for u in usuarios_sin_company:
                self.stdout.write(f"Usuario {u.username} ({u.role}) sin company asignada")
        else:
            self.stdout.write("[]  <-- Todos los usuarios cumplen con las reglas")
