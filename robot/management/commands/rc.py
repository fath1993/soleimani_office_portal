import time

from django.core.management import base

from robot.cron import check_requested_product_thread_is_active, check_product_warehouse_thread_is_active


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        while True:
            try:
                check_requested_product_thread_is_active()
                check_product_warehouse_thread_is_active()
            except Exception as e:
                print(e)
            time.sleep(60)
