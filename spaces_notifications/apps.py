from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .utils import create_notice_types

class SpacesNotificationsConfig(AppConfig):
    name = 'spaces_notifications'

    def ready(self):
        #from .utils import register_notification
        #from django.utils.translation import ugettext_noop as _
        #register_notification(
        #    'default',
        #    _('Change Notification'),
        #    _('Something has changed in one of your groups.')
        #)
        post_migrate.connect(create_notice_types, sender=self)
