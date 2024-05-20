import jdatetime

from automation.tasks import CheckRequestedProductThread, CheckProductWarehouseThread
from custom_logs.models import custom_log
from robot.models import RequestedProductThreadIsActive, ProductWarehouseThreadIsActive

"""
crontab task start
"""


def check_requested_product_thread_is_active():
    now = jdatetime.datetime.now()
    now_minus_one_hour = now - jdatetime.timedelta(hours=1)
    threads = RequestedProductThreadIsActive.objects.filter()
    if threads.count() == 0:
        thread = RequestedProductThreadIsActive.objects.create()
    else:
        thread = threads.latest('id')
    if not now_minus_one_hour < thread.updated_at < now:
        custom_log("start CheckRequestedProductThread")
        CheckRequestedProductThread(name='check_requested_product_thread').start()


def check_product_warehouse_thread_is_active():
    now = jdatetime.datetime.now()
    now_minus_three_hour = now - jdatetime.timedelta(hours=3)
    threads = ProductWarehouseThreadIsActive.objects.filter()
    if threads.count() == 0:
        thread = ProductWarehouseThreadIsActive.objects.create()
    else:
        thread = threads.latest('id')
    if not now_minus_three_hour < thread.updated_at < now:
        custom_log("start CheckProductWarehouseThread")
        CheckProductWarehouseThread(name='check_product_warehouse_thread').start()



"""
crontab task end
"""
