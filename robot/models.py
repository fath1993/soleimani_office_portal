from django.db import models
from django_jalali.db import models as jmodel


class RequestedProductThreadIsActive(models.Model):
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='بروز شده در')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'بررسی محصول سیستم'
        verbose_name_plural = 'بررسی محصول سیستم'


class ProductWarehouseThreadIsActive(models.Model):
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='بروز شده در')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'بررسی انبار سیستم'
        verbose_name_plural = 'بررسی انبار سیستم'