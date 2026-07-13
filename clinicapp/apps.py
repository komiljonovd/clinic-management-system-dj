from django.apps import AppConfig


class ClinicappConfig(AppConfig):
    name = 'clinicapp'
    verbose_name = 'Clinic Management System'

    def ready(self):
        from . import signals
