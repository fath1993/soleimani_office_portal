import random
import threading
import time

import jdatetime

from accounts.models import Profile
from automation.models import RequestedProductProcessing, RequestedProduct
from custom_logs.models import custom_log


class AutomationMainFunctionThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        active_threads = threading.enumerate()
        threads_name_list = []
        for thread in active_threads:
            if thread.is_alive():
                threads_name_list.append(str(thread.name))
        if not 'general_functions_thread' in threads_name_list:
            custom_log("general_functions: start GeneralFunctionsThread")
            GeneralFunctionsThread(name='general_functions_thread').start()
            time.sleep(1)
        return


class GeneralFunctionsThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        active_threads = threading.enumerate()
        threads_name_list = []
        for thread in active_threads:
            if thread.is_alive():
                threads_name_list.append(str(thread.name))
        if not 'check_requested_product_thread' in threads_name_list:
            custom_log("general_functions: start CheckRequestedProductThread")
            CheckRequestedProductThread(name='check_requested_product_thread').start()
            time.sleep(1)

        if not 'check_product_warehouse_thread' in threads_name_list:
            custom_log("general_functions: start CheckProductWarehouseThread")
            CheckProductWarehouseThread(name='check_product_warehouse_thread').start()
            time.sleep(1)



class CheckRequestedProductThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        custom_log("CheckRequestedProductThread: start thread")
        while True:
            try:
                custom_log("check_requested_product: has been started")
                check_requested_product()
                custom_log("check_requested_product: has been finished.  waiting for 15 minutes")
                time.sleep(900)
            except Exception as e:
                custom_log(f"check_requested_product:try/except-> err: {str(e)}.  waiting for 5 seconds")
                time.sleep(5)


class CheckProductWarehouseThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        custom_log("CheckProductWarehouseThread: start thread")
        while True:
            try:
                custom_log("check_product_warehouse: has been started")
                check_product_warehouse()
                custom_log("check_product_warehouse: has been finished. waiting for 1 hour")
                time.sleep(3600)
            except Exception as e:
                custom_log(f"check_product_warehouse:try/except-> err: {str(e)}.  waiting for 5 seconds")
                time.sleep(5)


def check_requested_product():
    sales_allowed_users = Profile.objects.filter(daily_allowed_product_processing_number__gte=0)
    sales_allowed_user_with_available_quantity = []

    requested_products = RequestedProduct.objects.filter(is_product_available_at_warehouse=True, is_processed=False)
    for requested_product in requested_products:
        for sales_allowed_user in sales_allowed_users:
            user = sales_allowed_user.user
            now = jdatetime.datetime.now()
            start_of_today = jdatetime.datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
            all_request_product_processing_that_belong_to_user = RequestedProductProcessing.objects.filter(
                created_at__gte=start_of_today, seller=user)
            if all_request_product_processing_that_belong_to_user.count() < sales_allowed_user.daily_allowed_product_processing_number:
                sales_allowed_user_with_available_quantity.append(user)
        if len(sales_allowed_user_with_available_quantity) > 0:
            RequestedProductProcessing.objects.create(
                requested_product=requested_product,
                seller=random.choice(sales_allowed_user_with_available_quantity),
            )
        time.sleep(0.1)


def check_product_warehouse():
    requested_products = RequestedProduct.objects.filter(is_product_available_at_warehouse=False, is_processed=True)
    for requested_product in requested_products:
        product = requested_product.product
        if product.product_warehouse.available_number > 0:
            requested_product.is_product_available_at_warehouse = True
            requested_product.is_processed = False
            requested_product.save()



