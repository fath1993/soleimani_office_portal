from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from gallery.models import FileGallery

PRODUCT_TYPE = (('کالا', 'کالا'), ('خدمات', 'خدمات'),)
CREATOR_CONTENT_TYPE = (('صوتی', 'صوتی'), ('تصویری', 'تصویری'), ('ویدیویی', 'ویدیویی'), ('متنی', 'متنی'),
                        ('تلفیقی', 'تلفیقی'), ('اینستاگرامی', 'اینستاگرامی'),)
RESELLER_NETWORK_TYPE = (('ماهواره', 'ماهواره'), ('تلویزیون', 'تلویزیون'), ('شبکه اجتماعی', 'شبکه اجتماعی'),)
RESELLER_NETWORK_BROADCAST_DIRECTION = (('یاه ست', 'یاه ست'), ('هات برد', 'هات برد'),
                                        ('ترکمن عالم', 'ترکمن عالم'),)
RECEIVER_RECEIVING_TYPE = (('شماره موبایل', 'شماره موبایل'), ('شماره سامانه', 'شماره سامانه'),
                           ('Qr Code', 'Qr Code'), ('لینک', 'لینک'),
                           ('صفحه فرود شبکه اجتماعی', 'صفحه فرود شبکه اجتماعی'),
                           ('صفحه فرود فروشگاه اینترنتی', 'صفحه فرود فروشگاه اینترنتی'),)
ADVERTISE_CONTENT_TYPE = (('محتوای ویدیویی تلویزیون', 'محتوای ویدیویی تلویزیون'),
                          ('محتوای ویدیویی ماهواره', 'محتوای ویدیویی ماهواره'),
                          ('محتوای ویدیویی شبکه اجتماعی', 'محتوای ویدیویی شبکه اجتماعی'),
                          ('محتوای تصویری', 'محتوای تصویری'), ('محتوای متنی (زیرنویس)', 'محتوای متنی (زیرنویس)'),
                          ('محتوای صوتی (نریشن)', 'محتوای صوتی (نریشن)'),)

COMMUNICATION_CHANNEL_TYPE = (('سامانه پیامکی', 'سامانه پیامکی'), ('ربات تلگرام', 'ربات تلگرام'),)
REGISTER_TYPE = (('تخصیص دستی', 'تخصیص دستی'), ('تخصیص خودکار', 'تخصیص خودکار'),
                 ('تخصیص خودکار بر اساس عملکرد', 'تخصیص خودکار بر اساس عملکرد'),)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE, default='کالا', null=False, blank=False,
                            verbose_name='نوع محصول')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    weight = models.IntegerField(default=0, null=False, blank=False, verbose_name='وزن - گرم')
    size = models.FloatField(default=0, null=False, blank=False, verbose_name='سایز - اینچ')
    color = models.CharField(max_length=255, null=False, blank=False, verbose_name='رنگ')
    images = models.ManyToManyField(FileGallery, related_name='images_product', blank=True, verbose_name='تصاویر')
    videos = models.ManyToManyField(FileGallery, related_name='videos_product', blank=True, verbose_name='ویدیو ها')

    product_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه خام محصول - ریال')
    shipping_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه حمل - ریال')
    send_link_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه ارسال لینک - ریال')
    packing_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه بسته بندی - ریال')
    seller_commission = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=False, blank=False,
                                            verbose_name='کمیسیون فروشنده - درصد')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_product', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_product', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


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


class TeaserMaker(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    content_type = models.CharField(max_length=255, choices=CREATOR_CONTENT_TYPE, default='صوتی', null=False,
                                    blank=False,
                                    verbose_name='نوع محتوا')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    address = models.CharField(max_length=2000, null=False, blank=False, verbose_name='آدرس')
    phone_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره تماس')

    creation_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه ساخت - ریال')
    editing_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه ویرایش - ریال')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_creator', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_creator', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'تیزر ساز'
        verbose_name_plural = 'تیزر ساز ها'


class ResellerNetwork(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    network_type = models.CharField(max_length=255, choices=RESELLER_NETWORK_TYPE, default='ماهواره', null=False,
                                    blank=False,
                                    verbose_name='نوع محتوا')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    broadcast_direction = models.CharField(max_length=255, choices=RESELLER_NETWORK_BROADCAST_DIRECTION,
                                           default='ماهواره', null=False,
                                           blank=False,
                                           verbose_name='جهت پخش')

    company_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام کمپانی')
    owner_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام صاحب')
    broker_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام واسط')

    broadcast_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه پخش - ریال')
    subtitle_price = models.IntegerField(default=0, null=False, blank=False, verbose_name='هزینه زیرنویس - ریال')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_reseller_network', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_reseller_network', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'شبکه'
        verbose_name_plural = 'شبکه ها'


class Receiver(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    receiving_type = models.CharField(max_length=255, choices=RECEIVER_RECEIVING_TYPE, default='شماره موبایل',
                                      null=False,
                                      blank=False,
                                      verbose_name='نوع دریافت')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    receiver_phone_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره')

    price = models.IntegerField(default=0, null=False, blank=False, verbose_name='قیمت - ریال')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_receiver', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_receiver', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'دریافت کننده'
        verbose_name_plural = 'دریافت کننده ها'


class AdvertiseContent(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    advertise_content_type = models.CharField(max_length=255, choices=ADVERTISE_CONTENT_TYPE,
                                              default='محتوای ویدیویی تلویزیون', null=False, blank=False,
                                              verbose_name='نوع محتوای تبلیغ')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    content = models.ManyToManyField(FileGallery, related_name='content_advertise_content', blank=True,
                                     verbose_name='محتوا')

    product = models.ForeignKey(Product, related_name='product_advertise_content', on_delete=models.CASCADE, null=False,
                                blank=False, verbose_name='محصول')
    receiver = models.ForeignKey(Receiver, related_name='receiver_advertise_content', on_delete=models.CASCADE,
                                 null=False, blank=False, verbose_name='دریافت کننده')
    teaser_maker = models.ForeignKey(TeaserMaker, related_name='teaser_maker_advertise_content',
                                     on_delete=models.CASCADE, null=False, blank=False, verbose_name='تیزر ساز')
    reseller_network = models.ForeignKey(ResellerNetwork, related_name='reseller_network_advertise_content',
                                         on_delete=models.CASCADE, null=False, blank=False,
                                         verbose_name='شبکه تبلیغ کننده')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_advertise_content', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_advertise_content', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'محتوای تبلیغاتی'
        verbose_name_plural = 'محتوا های تبلیغاتی'


class ForwardToPortal(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    communication_type = models.CharField(max_length=255, choices=COMMUNICATION_CHANNEL_TYPE, default='سامانه پیامکی',
                                          null=False,
                                          blank=False,
                                          verbose_name='نوع کانال ارتباطی')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    address = models.CharField(max_length=3000, null=False, blank=False, verbose_name='آدرس')
    price = models.IntegerField(default=0, null=False, blank=False, verbose_name='قیمت - ریال')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_forward_to_portal', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_forward_to_portal', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'انتقال دهنده'
        verbose_name_plural = 'انتقال دهندگان'


class CommunicationChannel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    communication_type = models.CharField(max_length=255, choices=COMMUNICATION_CHANNEL_TYPE, default='سامانه پیامکی',
                                          null=False,
                                          blank=False,
                                          verbose_name='نوع کانال ارتباطی')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')
    phone_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='شماره')
    price = models.IntegerField(default=0, null=False, blank=False, verbose_name='قیمت - ریال')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_communication_channel', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_communication_channel', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'کانال ارتباطی'
        verbose_name_plural = 'کانال های ارتباطی'


class Registrar(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    register_type = models.CharField(max_length=255, choices=REGISTER_TYPE, default='تخصیص دستی',
                                     null=False,
                                     blank=False,
                                     verbose_name='نوع تخصیص')
    code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروزرسانی')
    created_by = models.ForeignKey(User, related_name='created_by_registrar', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(User, related_name='updated_by_registrar', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    is_active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'name: {self.name} | code: {self.code}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'تخصیص دهنده'
        verbose_name_plural = 'تخصیص دهنده ها'



