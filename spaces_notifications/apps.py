from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .utils import create_notice_types

class SpacesNotificationsConfig(AppConfig):
    name = 'spaces_notifications'

    def ready(self):
        post_migrate.connect(create_notice_types, sender=self)
