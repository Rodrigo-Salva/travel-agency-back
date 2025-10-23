from django.apps import AppConfig


class InquiriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.inquiries'
    verbose_name = 'Consultas'
    
    def ready(self):
        pass