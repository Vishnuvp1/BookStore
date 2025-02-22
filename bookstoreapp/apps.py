from django.apps import AppConfig


class BookstoreappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookstoreapp"

    def ready(self):
        import bookstoreapp.signals  # Import signals module
