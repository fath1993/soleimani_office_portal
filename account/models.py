from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel


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


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

