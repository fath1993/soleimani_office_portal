from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from tickets.models import Notification

HAS_ACCESS_TO_SECTION = (('user', 'کاربر'), ('permission', 'مجوز'), ('role', 'نقش'),
                         ('resource', 'منابع'), ('product', 'محصولات'), ('teaser_maker', 'تیزر ساز'),
                         ('reseller_network', 'شبکه'),
                         ('receiver', 'دریافت کننده'), ('advertise_content', 'محتوای تبلیغاتی'),
                         ('forward_to_portal', 'انتقال دهنده'), ('communication_channel', 'کانال ارتباطی'),
                         ('registrar', 'تخصیص دهنده'),
                         ('automation', 'اتوماسیون'),
                         ('automation_project', 'اتوماسیون - ساخت پروژه'),
                         ('automation_task', 'اتوماسیون - ایجاد وظیفه'),
                         ('automation_communicate', 'اتوماسیون - مکاتبات'),
                         ('ticket_admin', 'تیکت ادمین'),
                         ('ticket', 'تیکت'), ('message', 'پیام'),
                         ('notification', 'اطلاعیه'),)


class Permission(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    has_access_to_section = models.CharField(max_length=255, choices=HAS_ACCESS_TO_SECTION, null=False, blank=False,
                                             verbose_name='دسترسی به بخش')
    read = models.BooleanField(default=True, verbose_name='خواندن')
    create = models.BooleanField(default=True, verbose_name='ایجاد')
    modify = models.BooleanField(default=True, verbose_name='ویرایش')
    delete = models.BooleanField(default=True, verbose_name='حذف')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسترسی'
        verbose_name_plural = 'دسترسی ها'


class Role(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name='اجازه ها')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'نقش'
        verbose_name_plural = 'نقش ها'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, null=False, blank=False,
                                editable=False, verbose_name='کاربر')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='کد ملی')
    mobile_phone_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره همراه')
    landline = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره ثابت')
    birthday = jmodel.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره کارت')
    isbn = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره شبا')
    address = models.CharField(max_length=1000, null=True, blank=True, verbose_name='آدرس')

    role = models.ForeignKey(Role, related_name='profile_roles', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='نقش')

    daily_allowed_product_processing_number = models.IntegerField(default=0, null=False, blank=False, verbose_name='تعداد مجاز فروش محصولات روزانه')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            permission = Permission.objects.get_or_create(title='همه')
            new_profile = Profile.objects.create(user=instance)
            new_profile.role.add(permission[0])
            new_profile.save()

        else:
            Profile.objects.create(user=instance)


class UserNotification(models.Model):
    user = models.ForeignKey(User, related_name='user_user_notification', on_delete=models.CASCADE, null=False,
                             blank=False,
                             editable=False, verbose_name='کاربر')
    notification = models.ForeignKey(Notification, related_name='notification_user_notification',
                                     on_delete=models.CASCADE, null=False,
                                     blank=False,
                                     editable=False, verbose_name='اطلاعیه')
    has_seen_by_user = models.BooleanField(default=False, verbose_name='دیده شده توسط کاربر')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اطلاعیه کاربر'
        verbose_name_plural = 'اطلاعیه های کاربران'
