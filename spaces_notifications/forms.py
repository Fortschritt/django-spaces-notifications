#from functools import partial, wraps
from django import forms
from django.forms import formset_factory
from django.utils.functional import curry
from django.utils.translation import ugettext as _


class NotificationForm(forms.Form):
    """
    provide a list of possible recipients of a notification
    """
    def __init__(self, space=None, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        if space:

            n12n_choices = (
                ('all', _('Notify all members')),
                ('team', _('Notify team')),
                ('admins', _('Notify admins')),
            )
            self.fields['notify_by_role'] = forms.MultipleChoiceField(
                choices=n12n_choices,
                widget=forms.CheckboxSelectMultiple(
                    attrs = {
                        'class': 'n12n-role',
                    }
                ),
                required=False,
            )
            members = space.get_members()
            member_qs = members.user_set.all()
            self.fields['notify_these_members'] = forms.ModelMultipleChoiceField(
                queryset=member_qs, 
                widget=forms.CheckboxSelectMultiple(
                    attrs = {
                        'class': 'n12n-user',
                    }
                ),
                required=False,
            )

    class Media:
        css = {
            'all': ()
        }
        js = ("spaces_notifications/js/n12n.js",
             )


def NotificationFormSet(space,  *args, **kwargs):
    """
    we need to pass in the current space to NotificationForm, which is easy by itself
    but tricky inside a formset.
    
    """
    FormSet = formset_factory(NotificationForm)
    FormSet.form = staticmethod(curry(NotificationForm, space=space))
    return FormSet(*args, **kwargs)
