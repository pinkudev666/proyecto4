from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def set_role_for_superuser(sender, instance, created, **kwargs):
    """
    Si se crea un superuser (via createsuperuser) y role está vacío -> asignar 'super_admin'.
    También útil si se crea user.is_superuser=True en cualquier otro flujo.
    """
    try:
        if instance.is_superuser and (instance.role is None or instance.role == ""):
            instance.role = 'super_admin'
            # evitar recursividad del signal porque post_save se ejecuta otra vez;
            # update_fields evita ejecutar otros saves innecesarios
            instance.save(update_fields=['role'])
    except Exception:
        # no romper el flujo por un error ocasional
        pass
