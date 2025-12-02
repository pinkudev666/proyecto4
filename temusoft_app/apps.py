from django.apps import AppConfig


class TemusoftAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'temusoft_app'

    def ready(self):
        # importa signals para que se registren
        import temusoft_app.signals  # noqa: F401