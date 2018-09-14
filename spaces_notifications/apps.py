from django.apps import AppConfig

class SpacesNotificationsConfig(AppConfig):
    name = 'spaces_notifications'

    def ready(self):
        from .utils import register_notification
        from django.utils.translation import ugettext_noop as _
        register_notification(
            'default',
            _('Change Notification'),
            _('Something has changed in one of your groups.')
        )
