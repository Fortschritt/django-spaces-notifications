from django import template
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

register = template.Library()

@register.filter(name="is_id_admin")
def is_id_admin(user_id, space):
    """
    Returns True if the given user id has the 'admin' role for the given space,
    else False. 

    Usage example:

    {% if user_id|is_id_admin:space %}Space Admin{% endif %}

    Is only True if the user is a member of the 'admin' group of this space.
    """
    if user_id and space:
        admins = space.get_admins().user_set.all()
        user = User.objects.get(id=user_id)
    else:
        return False
    ret = False
    if user in admins or (hasattr(user, 'collab') and user.collab.is_manager) \
        or user.is_superuser:
        ret = True
    return ret

@register.filter(name="is_id_team")
def is_id_team(user_id, space):
    """
    Returns True if the given user id has the 'team' role for the given space,
    else False. 

    Usage example:

    {% if user_id|is_id_team:space %}Space Team{% endif %}

    Is only True if the user is a member of the 'admin' group of this space.
    """
    if user_id and space:
        admins = space.get_team().user_set.all()
        user = User.objects.get(id=user_id)
    else:
        return False
    ret = False
    if user in admins:
        ret = True
    return ret

