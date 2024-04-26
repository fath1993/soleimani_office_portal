from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel


class Project(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_project', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'name: {self.name}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم ها'


class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    description = models.TextField(null=False, blank=False, verbose_name='توضیحات')

    '''
    detail is json array with the bellow format:
    {
        [0]: {
            'detail_description': 'xxx',
            'created_at': 'xxx',
            'created_by': 'xxx',
            'previous_worker': 'xxx',
        },
        [1]: {
            'detail_description': 'xxx',
            'created_at': 'xxx',
            'created_by': 'xxx',
            'previous_worker': 'xxx',
        },
        ...
    }
    '''
    detail = models.TextField(null=True, blank=True, verbose_name='جزئیات')
    previous_worker = models.ForeignKey(User, related_name='task_previous_worker',
                                        on_delete=models.CASCADE, null=False,
                                        blank=False, editable=False, verbose_name='در حال اجرا توسط')
    current_worker = models.ForeignKey(User, related_name='task_current_worker',
                                       on_delete=models.CASCADE, null=False,
                                       blank=False, editable=False, verbose_name='در حال اجرا توسط')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_task', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'name: {self.name}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'وظیفه'
        verbose_name_plural = 'وظایف'
