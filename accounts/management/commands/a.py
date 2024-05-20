from django.core.management import base

from accounts.models import Role, Permission, Section


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        Section.objects.all().delete()
        Permission.objects.all().delete()
        Role.objects.all().delete()