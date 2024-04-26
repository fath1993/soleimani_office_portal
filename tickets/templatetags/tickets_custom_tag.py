from django import template
from django.db.models import Q
from tickets.models import Ticket

register = template.Library()


@register.filter
def ticket_admin_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
    if user.is_superuser:
        return True
    else:
        q = Q()
        if allowed_actions:
            allowed_actions = str(allowed_actions).split(',')
            for action in allowed_actions:
                q |= (
                    Q(**{f'{action}': True})
                )
        else:
            q &= (
                    Q(**{f'read': True}) |
                    Q(**{f'create': True}) |
                    Q(**{f'modify': True}) |
                    Q(**{f'delete': True})
            )
        q &= (Q(**{f'has_access_to_section': 'ticket_admin'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions



@register.filter
def ticket_count(request, count_type):
    if count_type == 'self':
        return Ticket.objects.filter(belong_to=request.user).count()
    if count_type == 'all':
        return Ticket.objects.all().count()
    return 0
