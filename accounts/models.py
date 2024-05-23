from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from tickets.models import Notification

SECTIONS = (('user', 'کاربر'), ('permission', 'مجوز'), ('role', 'نقش'),
            ('resource', 'منابع'), ('product', 'محصولات'), ('teaser_maker', 'تیزر ساز'),
            ('reseller_network', 'شبکه'),
            ('receiver', 'دریافت کننده'), ('advertise_content', 'محتوای تبلیغاتی'),
            ('forward_to_portal', 'انتقال دهنده'), ('communication_channel', 'کانال ارتباطی'),
            ('registrar', 'تخصیص دهنده'),
            ('ticket_admin', 'تیکت ادمین'),
            ('ticket', 'تیکت'),
            ('message', 'پیام'),
            ('notification', 'اطلاعیه'),
            ('sale', 'فروش'),
            ('warehouse', 'انبار'),
            ('delivery', 'ارسال'),)

ROLES = (('manager', 'مدیر'), ('user', 'کاربر'), ('seller', 'فروشنده'), ('warehouse_keeper', 'انباردار'),
         ('delivery_person', 'ارسال کننده'),)


class Section(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,
                            editable=False, verbose_name='نام')
    name_fa = models.CharField(max_length=255, null=False, blank=False,
                            editable=False, verbose_name='نام فارسی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'


class Permission(models.Model):
    has_access_to_section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                              related_name='has_access_to_section_permission',
                                              blank=False, verbose_name='دسترسی به بخش')
    read = models.BooleanField(default=True, verbose_name='خواندن')
    create = models.BooleanField(default=True, verbose_name='ایجاد')
    modify = models.BooleanField(default=True, verbose_name='ویرایش')
    delete = models.BooleanField(default=True, verbose_name='حذف')

    def __str__(self):
        string = f''''''
        if self.read:
            string += 'read, '
        if self.create:
            string += 'create, '
        if self.modify:
            string += 'modify, '
        if self.delete:
            string += 'delete, '
        return f'{self.has_access_to_section}: {string}'

    class Meta:
        ordering = ['id', ]
        verbose_name = 'اجازه'
        verbose_name_plural = 'اجازه ها'


class Role(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    role = models.CharField(max_length=255, default='user', choices=ROLES, null=False, blank=False,
                            verbose_name='نقش')
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name='اجازه ها')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id', ]
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

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='roles_profile', null=True, blank=True, verbose_name='نقش')


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


class SellerProfile(models.Model):
    profile = models.OneToOneField(Profile, related_name='profile_seller_profile', on_delete=models.CASCADE, null=False,
                                   blank=False,
                                   editable=False, verbose_name='پروفایل کاربر')
    is_sales_admin = models.BooleanField(default=False, verbose_name='ایا مدیر فروش است؟')
    daily_allowed_product_processing_number = models.PositiveIntegerField(default=0, null=False, blank=False,
                                                                          verbose_name='تعداد مجاز فروش محصولات روزانه')

    def __str__(self):
        return self.profile.user.username

    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'


class WarehouseProfile(models.Model):
    profile = models.OneToOneField(Profile, related_name='profile_warehouse_profile', on_delete=models.CASCADE, null=False,
                                   blank=False,
                                   editable=False, verbose_name='پروفایل کاربر')
    is_warehouse_admin = models.BooleanField(default=False, verbose_name='ایا مدیر انبار است؟')

    def __str__(self):
        return self.profile.user.username

    class Meta:
        verbose_name = 'انباردار'
        verbose_name_plural = 'انبار داران'


class DeliveryProfile(models.Model):
    profile = models.OneToOneField(Profile, related_name='profile_delivery_profile', on_delete=models.CASCADE, null=False,
                                   blank=False,
                                   editable=False, verbose_name='پروفایل کاربر')
    is_delivery_admin = models.BooleanField(default=False, verbose_name='ایا مدیر ارسال است؟')

    def __str__(self):
        return self.profile.user.username

    class Meta:
        verbose_name = 'ارسال کننده'
        verbose_name_plural = 'ارسال کنندگان'


@receiver(post_save, sender=Profile)
def update_extra_profile(sender, instance, created, **kwargs):
    profile = Profile.objects.get(user=instance.user)

    # seller
    seller_profile_is_needed = False
    permissions = profile.role.permissions.filter(has_access_to_section__name='sale', read=True, create=True)
    if permissions.exists():
        seller_profile_is_needed = True
    print(f'seller_profile_is_needed? {seller_profile_is_needed}')

    if seller_profile_is_needed:
        seller_profile, created = SellerProfile.objects.get_or_create(
            profile=profile,
        )

    if not seller_profile_is_needed:
        try:
            seller_profile = SellerProfile.objects.get(profile=profile)
            seller_profile.delete()
        except:
            pass

    # warehouse
    warehouse_profile_is_needed = False
    permissions = profile.role.permissions.filter(has_access_to_section__name='warehouse', read=True, create=True)
    if permissions.exists():
        warehouse_profile_is_needed = True
    print(f'warehouse_profile_is_needed? {warehouse_profile_is_needed}')

    if warehouse_profile_is_needed:
        warehouse_profile, created = WarehouseProfile.objects.get_or_create(
            profile=profile,
        )

    if not warehouse_profile_is_needed:
        try:
            warehouse_profile = WarehouseProfile.objects.get(profile=profile)
            warehouse_profile.delete()
        except:
            pass


    # delivery
    delivery_profile_is_needed = False
    permissions = profile.role.permissions.filter(has_access_to_section__name='delivery', read=True, create=True)
    if permissions.exists():
        delivery_profile_is_needed = True
    print(f'delivery_profile_is_needed? {delivery_profile_is_needed}')

    if delivery_profile_is_needed:
        delivery_profile, created = DeliveryProfile.objects.get_or_create(
            profile=profile,
        )

    if not delivery_profile_is_needed:
        try:
            delivery_profile = DeliveryProfile.objects.get(profile=profile)
            delivery_profile.delete()
        except:
            pass



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


@receiver(post_save, sender=User)
def auto_create_data(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            create_sections()
            create_permissions()
            create_roles()


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            role = get_or_create_manager_default_role_permission()
            profile = Profile.objects.create(user=instance, role=role)
        else:
            role = get_or_create_user_default_role_permission()
            profile = Profile.objects.create(user=instance, role=role)


def create_sections():
    for section_code, name in SECTIONS:
        section, created = Section.objects.get_or_create(
            name=section_code,
            name_fa=name,
        )


def update_sections():
    for section_code, name in SECTIONS:
        section, created = Section.objects.update_or_create(
            name=section_code,
            name_fa=name,
        )


def create_permissions():
    for section in Section.objects.all():
        # Iterate over all possible combinations of read, create, modify, and delete
        for read_value in [True, False]:
            for create_value in [True, False]:
                for modify_value in [True, False]:
                    for delete_value in [True, False]:
                        # Get or create the permission object with the current combination of values
                        permission, created = Permission.objects.get_or_create(
                            has_access_to_section=section,
                            read=read_value,
                            create=create_value,
                            modify=modify_value,
                            delete=delete_value,
                            defaults={
                                'read': read_value,
                                'create': create_value,
                                'modify': modify_value,
                                'delete': delete_value
                            }
                        )
                        print(permission)
                        print(created)
                        print('----------------------')


def update_permissions():
    for section in Section.objects.all():
        # Iterate over all possible combinations of read, create, modify, and delete
        for read_value in [True, False]:
            for create_value in [True, False]:
                for modify_value in [True, False]:
                    for delete_value in [True, False]:
                        # Get or create the permission object with the current combination of values
                        permission, created = Permission.objects.update_or_create(
                            has_access_to_section=section,
                            read=read_value,
                            create=create_value,
                            modify=modify_value,
                            delete=delete_value,
                            defaults={
                                'read': read_value,
                                'create': create_value,
                                'modify': modify_value,
                                'delete': delete_value
                            }
                        )
                        print(permission)
                        print(created)
                        print('----------------------')


def create_roles():
    get_or_create_user_default_role_permission()
    get_or_create_seller_default_role_permission()
    get_or_create_warehouse_keeper_default_role_permission()
    get_or_create_delivery_person_default_role_permission()
    get_or_create_manager_default_role_permission()



def get_or_create_manager_default_role_permission():
    permissions = Permission.objects.filter(read=True, create=True, modify=True, delete=True)
    try:
        role = Role.objects.get(title='ادمین کل - سیستم')
    except:
        role = Role.objects.create(
            title='ادمین کل - سیستم',
            role='manager',
        )
    for permission in permissions:
        role.permissions.add(permission)
    return role


def get_or_create_user_default_role_permission():
    try:
        role = Role.objects.get(title='کاربر - سیستم')
    except:
        role = Role.objects.create(
            title='کاربر - سیستم',
            role='user',
        )
    return role


def get_or_create_seller_default_role_permission():
    permissions = Permission.objects.filter(has_access_to_section__name='sale', read=True, create=True, modify=True, delete=True)
    try:
        role = Role.objects.get(title='فروشنده - سیستم')
    except:
        role = Role.objects.create(
            title='فروشنده - سیستم',
            role='seller',
        )
    for permission in permissions:
        role.permissions.add(permission)
    return role


def get_or_create_warehouse_keeper_default_role_permission():
    permissions = Permission.objects.filter(has_access_to_section__name='warehouse', read=True, create=True, modify=True, delete=True)
    try:
        role = Role.objects.get(title='انباردار - سیستم')
    except:
        role = Role.objects.create(
            title='انباردار - سیستم',
            role='warehouse_keeper',
        )
    for permission in permissions:
        role.permissions.add(permission)
    return role


def get_or_create_delivery_person_default_role_permission():
    permissions = Permission.objects.filter(has_access_to_section__name='delivery', read=True, create=True, modify=True, delete=True)
    try:
        role = Role.objects.get(title='ارسال کننده - سیستم')
    except:
        role = Role.objects.create(
            title='ارسال کننده - سیستم',
            role='delivery_person',
        )
    for permission in permissions:
        role.permissions.add(permission)
    return role



