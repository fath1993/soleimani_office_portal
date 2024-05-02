from django.core.management import base

from tickets.models import Ticket


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        Ticket.objects.all().delete()