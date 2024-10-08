from django import template
from django.contrib.auth.models import User
from django.db.models import Q

from accounts.models import Role, Permission, Section, Profile
from resource.models import Product, TeaserMaker, ResellerNetwork, Receiver, AdvertiseContent, ForwardToPortal, \
    CommunicationChannel, Registrar

register = template.Library()


@register.filter
def role_list(request):
    return Role.objects.filter()


@register.filter
def profile_list(request):
    return Profile.objects.filter()


@register.filter
def advertise_content_list(request):
    return AdvertiseContent.objects.filter()


@register.filter
def receiver_list(request):
    return Receiver.objects.filter()


@register.filter
def product_list(request):
    return Product.objects.filter()


@register.filter
def teaser_maker_list(request):
    return TeaserMaker.objects.filter()


@register.filter
def reseller_network_list(request):
    return ResellerNetwork.objects.filter()


@register.filter
def object_count(request, count_type):
    if count_type == 'user':
        return User.objects.all().count()
    if count_type == 'permission':
        return Permission.objects.all().count()
    if count_type == 'role':
        return Role.objects.all().count()
    if count_type == 'product':
        return Product.objects.all().count()
    if count_type == 'teaser-maker':
        return TeaserMaker.objects.all().count()
    if count_type == 'reseller-network':
        return ResellerNetwork.objects.all().count()
    if count_type == 'receiver':
        return Receiver.objects.all().count()
    if count_type == 'advertise-content':
        return AdvertiseContent.objects.all().count()
    if count_type == 'forward-to-portal':
        return ForwardToPortal.objects.all().count()
    if count_type == 'communication-channel':
        return CommunicationChannel.objects.all().count()
    if count_type == 'registrar':
        return Registrar.objects.all().count()
    return 0