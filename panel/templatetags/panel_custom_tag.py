from django import template
from django.db.models import Q

from accounts.models import Role

register = template.Library()


@register.filter
def user_section_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify,delete
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
        q &= (Q(**{f'has_access_to_section': 'user'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def permission_section_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
    if user.is_superuser:
        return True
    else:
        q = Q()
        if allowed_actions:
            allowed_actions = str(allowed_actions).split(',')
            for action in allowed_actions:
                q &= (
                    Q(**{f'{action}': True})
                )
        else:
            q &= (
                    Q(**{f'read': True}) |
                    Q(**{f'create': True}) |
                    Q(**{f'modify': True}) |
                    Q(**{f'delete': True})
            )
        q &= (Q(**{f'has_access_to_section': 'permission'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def role_section_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'role'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions



@register.filter
def resource_section_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'resource'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def product_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'product'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def teaser_maker_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'teaser_maker'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def reseller_network_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'reseller_network'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def receiver_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'receiver'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def advertise_content_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'advertise_content'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def forward_to_portal_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'forward_to_portal'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def communication_channel_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'communication_channel'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def registrar_is_allowed(user, allowed_actions=None):  # allowed actions should be like read,create,modify
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
        q &= (Q(**{f'has_access_to_section': 'registrar'}))
        permissions = user.user_profile.role.permissions.filter(q).exists()
        return permissions


@register.filter
def role_list(request):
    return Role.objects.filter()
