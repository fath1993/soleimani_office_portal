from django.apps import AppConfig


class CustomLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_logs'
    verbose_name = '00- لاگ'
    verbose_name_plural = '00- لاگ'
