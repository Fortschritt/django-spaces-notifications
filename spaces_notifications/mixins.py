from django.views.generic.base import TemplateResponseMixin
from pinax.notifications.models import send
from .forms import NotificationFormSet

def send_manual_notification(user, label, object_title='', object_link=''):
    """
    Manually send out a notification email to user
    """
    send([user], label, {
            'space_url': '',
            'object_title': object_title,
            'object_link': object_link,
        })
    

def process_n12n_formset(formset, label, space, object_title='', object_link=''):
    """
    Process a filled NotificationFormset. Standalone so it can be used
    both in a class-based mixin and a functional view, keeping the codebase
    DRY.
    parameters: the formset, the notification label and the current Space.
                optionally title and link of the object to notify about
    """
    if formset.is_valid():
        if 'notify_these_members' in formset.cleaned_data[0].keys():
            users = list(formset.cleaned_data[0]['notify_these_members'])
        else:
            users = []
        role_users = {
            'all': space.get_members().user_set.all(),
            'team': space.get_team().user_set.all(),
            'admins': space.get_admins().user_set.all()
        }
        if 'notify_by_role' in formset.cleaned_data[0]:
            for role in formset.cleaned_data[0]['notify_by_role']:
                if role in role_users.keys():
                    users.extend(role_users[role])
        users = set(users) # ensure no user gets multiple mail
        #from pinax.notifications.models import NoticeType
        send(users, label, {
            'space_url':space.get_absolute_url(),
            'object_title': object_title,
            'object_link': object_link,
        })
    else:
        print(formset.errors)



class NotificationMixin(object):
    """ 
    A Mixin for sending out email notifications to users.
    Include the mixin in your CBV, set notification_* variables, and a mail will be sent
    automatically once form_valid is called.
    Alternatively (e.g. in situations where you can't include the mixin late enough in the
    inheritance order or some other class breaks the method chaining by not calling super())
    you can explicitely call self.send_notification().
    """

    notification_label = 'default'
    notification_object_title = ''
    notification_object_link = ''
    notification_send_manually = False # don't automatically send once form_valid() is called
    
    def get_context_data(self, **kwargs):
        context = super(NotificationMixin, self).get_context_data(**kwargs)
        if self.request.POST:
            formset =  NotificationFormSet(self.request.SPACE, self.request.POST)
            context['notification_formset'] = formset

        else:
            context['notification_formset'] = NotificationFormSet(self.request.SPACE)
        return context

    def form_valid(self, form):
        ret = super(NotificationMixin, self).form_valid(form)
        # extract all users that will get notified
        self.notification_formset = self.get_context_data()['notification_formset']
        self.notification_space = self.request.SPACE
        if not self.notification_send_manually:
            self.send_notification()
        return ret

    def send_notification(self):
        label = self.notification_label
        object_title = self.notification_object_title
        object_link = self.notification_object_link
        formset = self.notification_formset
        space = self.notification_space
        process_n12n_formset(formset, label, space, object_title=object_title,
                object_link = object_link)
