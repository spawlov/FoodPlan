from django.apps import AppConfig


class FoodAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food_app'
    verbose_name = 'Food for Life'

    def ready(self):
        from . import signals
