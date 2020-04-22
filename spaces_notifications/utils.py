from django.conf import settings
from django.utils.translation import ugettext_noop as _

def register_notification(label, display, description):
    #if db_table_exists('notifications_noticetype'):
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        NoticeType.objects.get_or_create(
            label=label, 
            display=display, 
            description=description,
            default=2 # sadly hardcoded, see the named parameter 'default' in NoticeType.create()
        )


def create_notice_types(sender, **kwargs): 
    if "pinax.notifications" in settings.INSTALLED_APPS:
        register_notification(
            'default',
            _('Change Notification'),
            _('Something has changed in one of your groups.')
        )

