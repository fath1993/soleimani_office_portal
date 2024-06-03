import random
import time

import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from accounts.models import SellerProfile, WarehouseProfile, DeliveryProfile, Profile
from resource.models import Product, Receiver

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


class ProductWarehouse(models.Model):
    product = models.OneToOneField(Product, related_name='product_product_warehouse', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='محصول')
    available_number = models.IntegerField(default=0, null=False, blank=False, verbose_name='تعداد موجودی')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_product_warehouse', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_product_warehouse', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'product: {self.product.name} | code: {self.product.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'اطلاعات جانبی محصول'
        verbose_name_plural = 'اطلاعات جانبی محصولات'


@receiver(post_save, sender=Product)
def auto_create_product_profile(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.get(username='admin')
        ProductWarehouse.objects.create(
            product=instance,
            created_by=admin,
            updated_by=admin,
        )


class CreditCard(models.Model):
    bank_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام بانک')
    account_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره حساب')
    card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره کارت')
    isbn = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره شبا')
    owner = models.ForeignKey(Profile, related_name='owner_credit_card', on_delete=models.CASCADE, null=False,
                              blank=False, verbose_name='مالک')
    brokers = models.ManyToManyField(Profile, related_name='brokers_credit_card', blank=True, verbose_name='کارگزاران')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_credit_card', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_credit_card', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

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
    in_department_status = models.CharField(max_length=255, default='sale',
                                            choices=REQUESTED_PRODUCT_PROCESSING_IN_DEPARTMENT_STATUS,
                                            null=False,
                                            blank=False, verbose_name='واحد فعلی پردازش کننده محصول')
    '''sales department'''
    # assign by system
    seller = models.ForeignKey(SellerProfile, related_name='seller_requested_product_processing',
                               on_delete=models.CASCADE, null=True,
                               blank=True, editable=False, verbose_name='اختصاص یافته به')
    # can change by sales department manager
    is_confirmed_by_sales_department = models.BooleanField(default=False, verbose_name='تایید واحد فروش')

    # can change by seller
    sales_status = models.CharField(max_length=255, default='processing', choices=REQUESTED_PRODUCT_SALES_STATUS,
                                    null=False,
                                    blank=False, verbose_name='وضعیت فروش محصول درخواستی')
    cancel_number = models.IntegerField(default=0, null=False, blank=False, verbose_name='تعداد کنسلی ها')
    cancel_multiply = models.IntegerField(default=0, null=False, blank=False,
                                          verbose_name='تعداد دفعات کنسلی با تغییر فروشنده')

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


class RequestedProductProcessingCancelReport(models.Model):
    requested_product_processing = models.ForeignKey(RequestedProductProcessing,
                                                     related_name='requested_product_processing_requested_product_processing_cancel_report',
                                                     on_delete=models.CASCADE, null=False,
                                                     blank=False, editable=False, verbose_name='محصول درخواستی')

    seller = models.ForeignKey(SellerProfile, related_name='seller_requested_product_processing_cancel_report',
                               on_delete=models.CASCADE, null=True,
                               blank=True, editable=False, verbose_name='تلاش برای فروش توسط')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_requested_product_processing_cancel_report',
                                   on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'{self.requested_product_processing.id}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'کنسلی پردازش محصول درخواستی'
        verbose_name_plural = 'کنسلی های پردازش محصولات درخواستی'


def create_requested_product_processing_cancel_report(requested_product_processing, seller, created_by):
    RequestedProductProcessingCancelReport.objects.create(
        requested_product_processing=requested_product_processing,
        seller=seller,
        created_by=created_by
    )


def report_requested_product_processing_cancel_number(requested_product_processing, seller):
    return RequestedProductProcessingCancelReport.objects.filter(
        requested_product_processing=requested_product_processing,
        seller=seller,
    ).count()


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
    if department == 'sale':
        department = 'فروش'
    if department == 'warehouse':
        department = 'انبار'
    if department == 'delivery':
        department = 'ارسال'

    if status == 'pending':
        status = 'انتظار'
    if status == 'processing':
        status = 'پردازش'
    if status == 'sold':
        status = 'فروش'
    if status == 'canceled':
        status = 'کنسلی'
    if status == 'pending_sales_approval':
        status = 'در انتظار تایید مدیریت فروش'
    if status == 'confirmed':
        status = 'تایید شده'
    if status == 'recheck':
        status = 'نیاز به بازبینی'
    if status == 'change_seller':
        status = 'تغییر فروشنده'
    if status == 'sent_to_delivery':
        status = 'تحویل به واحد ارسال'
    if status == 'return_to_sales':
        status = 'بازگشت به واحد فروش'
    if status == 'delivered':
        status = 'تحویل سفارش به مشتری'
    if status == 'return_to_warehouse':
        status = 'بازگشت سفارش به واحد انبار'
    if status == 'myself':
        status = 'بازگشایی سفارش برای فروشنده'
    if status == 'everyone':
        status = 'آزادسازی پردازش سفارش برای همه'

    system_report = f'گزارش سیستمی از وضعیت *{status}* با شماره سفارش #{requested_product_processing.id} توسط واحد *{department}* ثبت گردید.'

    system_admin = User.objects.filter(is_superuser=True).latest('id')
    RequestedProductProcessingReport.objects.create(
        requested_product_processing=requested_product_processing,
        department=department,
        status=status,
        report=system_report,
        created_by=system_admin,
    )
    time.sleep(0.1)
    try:
        if report is not None:
            RequestedProductProcessingReport.objects.create(
                requested_product_processing=requested_product_processing,
                department=department,
                status=status,
                report=report,
                created_by=created_by,
            )
    except Exception as e:
        print(e)
        pass


def pick_seller(exclude_profile=None):
    sales_allowed_profiles = SellerProfile.objects.filter(daily_allowed_product_processing_number__gte=0).exclude(
        profile=exclude_profile)
    sales_allowed_profiles_with_available_quantity = []
    for sales_allowed_profile in sales_allowed_profiles:
        now = jdatetime.datetime.now()
        start_of_today = jdatetime.datetime(year=now.year, month=now.month, day=now.day, hour=0,
                                            minute=0, second=0)
        all_request_product_processing_that_belong_to_user = RequestedProductProcessing.objects.filter(
            created_at__gte=start_of_today, seller=sales_allowed_profile)
        if all_request_product_processing_that_belong_to_user.count() < sales_allowed_profile.daily_allowed_product_processing_number:
            sales_allowed_profiles_with_available_quantity.append(sales_allowed_profile)
    if len(sales_allowed_profiles_with_available_quantity) > 0:
        seller = random.choice(sales_allowed_profiles_with_available_quantity)
        return seller
    else:
        return None


def pick_warehouse_keeper(exclude_profile=None):
    warehouse_profiles = WarehouseProfile.objects.all().exclude(profile=exclude_profile)
    if warehouse_profiles.count() == 0:
        return None
    else:
        warehouse_profile = warehouse_profiles[random.randint(0, warehouse_profiles.count() - 1)]
        return warehouse_profile


def pick_delivery_man(exclude_profile=None):
    delivery_profiles = DeliveryProfile.objects.all().exclude(profile=exclude_profile)
    if delivery_profiles.count() == 0:
        return None
    else:
        delivery_profile = delivery_profiles[random.randint(0, delivery_profiles.count() - 1)]
        return delivery_profile
