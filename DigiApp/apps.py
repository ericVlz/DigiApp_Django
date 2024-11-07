from django.apps import AppConfig


class DigiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DigiApp'

    def ready(self):
        import DigiApp.signals 
