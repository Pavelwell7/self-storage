from django.apps import AppConfig


class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.storage'
    verbose_name = "Склады и Аренда"

    def ready(self):
        import apps.storage.signals
