from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def user_list(request):
    return User.objects.filter()