Template

innerhalb des Formulars kommt rein:

{% include "spaces_notifications/form.html" %}

Class based View:

from spaces_notifications.mixins import NotificationMixin
class ...(NotificationMixin, ...)
	# optional:
	self.notification_label = 'name_of_label'

wenn ein optionales label genommen werden soll (self.notification_label),
dann muss das in der apps.py definiert werden:

def ready(self):
	...
	# register a custom notification
    from spaces_notifications.utils import register_notification
    from django.utils.translation import ugettext_noop as _
    register_notification(
        'name_of_label',
        _('This message goes to the user'),
        _('This is the description for internal forms etc..')
    )

Troubleshooting: 

wenn das n12n form nicht auftaucht: 
* kontrolliere, ob du nicht form_valid und/oder get_context_data ueberschrieben hast, ohne die Vorgänger aufzurufen:
	super(..., self).form_valid(form)
* kontrolliere, ob der erste Aufruf nicht von einem anderen View geregelt wird (z.B. bei bei einem Kommentar-Formular) - in diesem Fall muss das NotificationMixin auch beim anderen View rein
* kontrolliere, ob dein View das ContextMixin drin hat