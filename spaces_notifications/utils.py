from collab.util import db_table_exists
from pinax.notifications.models import NoticeType

def register_notification(label, display, description):
    """
    """ 
    if db_table_exists('notifications_noticetype'):
        NoticeType.objects.get_or_create(
            label=label, 
            display=display, 
            description=description,
            default=2 # sadly hardcoded, see the named parameter 'default' in NoticeType.create()
        )