import random

import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel

from accounts.models import SellerProfile, WarehouseProfile, DeliveryProfile
from portal.models import Product, Receiver

REQUESTED_PRODUCT_PROCESSING_IN_DEPARTMENT_STATUS = (('sale', 'فروش'), ('warehouse', 'انبار'),
                                                     ('delivery', 'ارسال'))

REQUESTED_PRODUCT_SALES_STATUS = (('pending', 'در انتظار'), ('processing', 'در حال پردازش'),
                                  ('sold', 'فروخته شده'),
                                  ('canceled', 'کنسل شده'),
                                  ('pending_sales_approval', 'در انتظار تایید مدیریت فروش'))

REQUESTED_PRODUCT_WAREHOUSE_STATUS = (
    ('pending', 'در انتظار'), ('processing', 'در حال پردازش'), ('sent_to_delivery', 'تحویل به واحد ارسال'),
    ('return_to_sales', 'بازگشت به واحد فروش'))

REQUESTED_PRODUCT_DELIVERY_STATUS = (
    ('pending', 'در انتظار'), ('processing', 'در حال پردازش'), ('delivered', 'تحویل شده به مشتری'),
    ('return_to_warehouse', 'بازگشت به واحد انبار'))


class ProductRelation(models.Model):
    product = models.ForeignKey(Product, related_name='product_product_relation', on_delete=models.CASCADE, null=False,
                                blank=False, verbose_name='محصول')
    receiver = models.ForeignKey(Receiver, related_name='receiver_product_relation',
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name='دریافت کننده')
    number = models.PositiveSmallIntegerField(default=0, null=False, blank=False, verbose_name='شماره مرتبط')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_product_relation', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'product name: {self.product.name} | receiver network: {self.receiver.receiver_phone_number}'

    class Meta:
        unique_together = ('product', 'receiver', 'number')
        ordering = ['created_at', ]
        verbose_name = 'ارتباط محصول و دریافت کننده'
        verbose_name_plural = 'ارتباط محصولات و دریافت کنندگان'


class CreditCard(models.Model):
    bank_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام بانک')
    account_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره حساب')
    card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره کارت')
    isbn = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره شبا')
    owner = models.ForeignKey(User, related_name='owner_credit_card', on_delete=models.CASCADE, null=False,
                              blank=False, verbose_name='مالک')
    broker = models.ManyToManyField(User, related_name='broker_credit_card', blank=True, verbose_name='کارگزار')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_credit_card', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_credit_card', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'{self.id} | {self.bank_name}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'کارت بانکی'
        verbose_name_plural = 'کارت های بانکی'


class Customer(models.Model):
    phone_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره تماس')
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام کامل')
    age = models.CharField(max_length=255, null=True, blank=True, verbose_name='تاریخ تولد')
    address = models.CharField(max_length=1000, null=True, blank=True, verbose_name='آدرس')
    desired_product = models.ManyToManyField(Product, related_name='desired_product_customer',
                                             blank=True, verbose_name='محصولات مورد علاقه')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'


class RequestedProduct(models.Model):
    product = models.ForeignKey(Product, related_name='product_requested_product', on_delete=models.CASCADE, null=False,
                                blank=False, verbose_name='محصول')
    customer = models.ForeignKey(Customer, related_name='customer_requested_product', on_delete=models.CASCADE,
                                 null=False,
                                 blank=False, verbose_name='خریدار')
    is_product_available_at_warehouse = models.BooleanField(default=False, verbose_name='محصول در انبار موجود است؟')
    is_processed = models.BooleanField(default=False, verbose_name='پردازش شده')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'محصول درخواستی'
        verbose_name_plural = 'محصولات درخواستی'


class RequestedProductProcessing(models.Model):
    # is created by system
    requested_product = models.ForeignKey(RequestedProduct,
                                          related_name='requested_product_requested_product_processing',
                                          on_delete=models.CASCADE, null=False,
                                          blank=False, editable=False, verbose_name='محصول درخواستی')
    # can change by user
    in_department_status = models.CharField(max_length=255, default='sales',
                                            choices=REQUESTED_PRODUCT_PROCESSING_IN_DEPARTMENT_STATUS,
                                            null=False,
                                            blank=False, verbose_name='واحد فعلی پردازش کننده محصول')
    '''sales department'''
    # assign by system
    seller = models.ForeignKey(SellerProfile, related_name='seller_requested_product_processing',
                               on_delete=models.CASCADE, null=False,
                               blank=False, editable=False, verbose_name='اختصاص یافته به')
    # can change by sales department manager
    is_confirmed_by_sales_department = models.BooleanField(default=False, verbose_name='تایید واحد فروش')

    # can change by seller
    sales_status = models.CharField(max_length=255, default='processing', choices=REQUESTED_PRODUCT_SALES_STATUS,
                                    null=False,
                                    blank=False, verbose_name='وضعیت فروش محصول درخواستی')
    cancel_number = models.IntegerField(default=0, null=False, blank=False, verbose_name='تعداد کنسلی ها')
    product_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی واحد محصول فروخته شده - ریال')
    product_number = models.IntegerField(null=True, blank=True, verbose_name='تعداد محصول فروخته شده')
    request_total_income = models.IntegerField(null=True, blank=True, verbose_name='درآمد نهایی این درخواست - ریال')
    '''sales department'''

    '''warehouse department'''
    # assign by system
    warehouse_keeper = models.ForeignKey(WarehouseProfile, related_name='warehouse_keeper_requested_product_processing',
                                         on_delete=models.CASCADE, null=True,
                                         blank=True, editable=False, verbose_name='انباردار')
    # can change by warehouse_keeper
    warehouse_status = models.CharField(max_length=255, default='pending',
                                        choices=REQUESTED_PRODUCT_WAREHOUSE_STATUS,
                                        null=False,
                                        blank=False, verbose_name='وضعیت انبار محصول درخواستی')
    is_confirmed_by_warehouse_keeper = models.BooleanField(default=False, verbose_name='تایید واحد انبار')

    '''warehouse department'''

    '''delivery department'''
    # assign by system
    delivery_man = models.ForeignKey(DeliveryProfile, related_name='delivery_man_requested_product_processing',
                                     on_delete=models.CASCADE, null=True,
                                     blank=True, editable=False, verbose_name='اختصاص یافته به')
    # can change by delivery_man
    delivery_status = models.CharField(max_length=255, default='pending',
                                       choices=REQUESTED_PRODUCT_DELIVERY_STATUS,
                                       null=False,
                                       blank=False, verbose_name='وضعیت ارسال محصول درخواستی')
    is_confirmed_by_delivery_man = models.BooleanField(default=False, verbose_name='تایید واحد ارسال')

    '''delivery department'''

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    updated_by = models.ForeignKey(User, related_name='updated_by_requested_product_processing',
                                   on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'{self.requested_product.product.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پردازش محصول درخواستی'
        verbose_name_plural = 'پردازش محصولات درخواستی'


class RequestedProductProcessingReport(models.Model):
    requested_product_processing = models.ForeignKey(RequestedProductProcessing,
                                                     related_name='requested_product_processing_requested_product_processing_report',
                                                     on_delete=models.CASCADE, null=False,
                                                     blank=False, editable=False, verbose_name='محصول درخواستی پردازشی')
    department = models.CharField(max_length=255,
                                  choices=REQUESTED_PRODUCT_PROCESSING_IN_DEPARTMENT_STATUS,
                                  null=False,
                                  editable=False,
                                  blank=False, verbose_name='واحد پردازش کننده محصول')
    status = models.CharField(max_length=255,
                              null=False,
                              editable=False,
                              blank=False, verbose_name='وضعیت محصول')
    report = models.TextField(null=True, blank=True, verbose_name='گزارش')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_requested_product_processing_report',
                                   on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'{self.requested_product_processing.requested_product.product.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'گزارش پردازش محصول درخواستی'
        verbose_name_plural = 'گزارشات پردازش محصولات درخواستی'


def create_requested_product_processing_report(requested_product_processing, department, status, report=None,
                                               created_by=None, **kwargs):
    if report is None:
        report = f'گزارش سیستمی از {status} با شناسه {requested_product_processing.id} توسط دپارتمان {department} ثبت گردید.'

    if not created_by:
        created_by = User.objects.filter(is_superuser=True).latest('id')
    RequestedProductProcessingReport.objects.create(
        requested_product_processing=requested_product_processing,
        department=department,
        status=status,
        report=report,
        created_by=created_by,
    )


def pick_seller(exclude_profile=None):
    sales_allowed_profiles = SellerProfile.objects.filter(daily_allowed_product_processing_number__gte=0)
    sales_allowed_profiles_with_available_quantity = []
    for sales_allowed_profile in sales_allowed_profiles:
        now = jdatetime.datetime.now()
        start_of_today = jdatetime.datetime(year=now.year, month=now.month, day=now.day, hour=0,
                                            minute=0, second=0)
        all_request_product_processing_that_belong_to_user = RequestedProductProcessing.objects.filter(
            created_at__gte=start_of_today, seller=sales_allowed_profile)
        if all_request_product_processing_that_belong_to_user.count() < sales_allowed_profile.daily_allowed_product_processing_number:
            if sales_allowed_profile != exclude_profile:
                sales_allowed_profiles_with_available_quantity.append(sales_allowed_profile)
    if len(sales_allowed_profiles_with_available_quantity) > 0:
        seller = random.choice(sales_allowed_profiles_with_available_quantity)
        return seller
    else:
        return None
