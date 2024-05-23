from django import template
from django.contrib.auth.models import User
from django.db.models import Q

from accounts.models import Section

register = template.Library()


@register.filter
def has_access_to_section(request, allowed_actions_and_section):  # allowed actions should be like read,create,modify,delete,section_name
    if request.user.is_superuser:
        return True
    else:
        q = Q()
        allowed_actions_and_section = str(allowed_actions_and_section).split(',')
        if len(allowed_actions_and_section) == 0:
            return False
        elif len(allowed_actions_and_section) == 1:
            section = allowed_actions_and_section[0]
        else:
            section = allowed_actions_and_section[-1]
            allowed_actions = allowed_actions_and_section[:-1]
            for action in allowed_actions:
                q |= (
                    Q(**{f'{action}': True})
                )
        try:
            section = Section.objects.get(name=section)
            q &= (Q(**{f'has_access_to_section': section}))
        except:
            pass
        permissions = request.user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def user_list(request):
    return User.objects.filter()