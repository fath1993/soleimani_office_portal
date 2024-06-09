from django.contrib.auth.models import User
from django.core.management import base

from accounts.models import Role, Permission, Section
from accounts.tests import create_test_account, set_user_password


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        # Section.objects.all().delete()
        # Permission.objects.all().delete()
        # Role.objects.all().delete()
        #User.objects.all().delete()
        #create_test_account()
        set_user_password()