import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class FileGallery(models.Model):
    alt = models.CharField(max_length=255, null=False, blank=False, verbose_name='متن جایگزین فایل')
    file = models.FileField(upload_to='gallery/', null=True, blank=True, verbose_name='فایل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, editable=False,
                                   verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'{self.id} | {self.file.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'


@receiver(pre_delete, sender=FileGallery)
def delete_source_file(sender, instance, **kwargs):
    try:
        os.remove(instance.file.path)
    except:
        pass


def create_file(request, in_memory_file_content):
    new_file = FileGallery.objects.create(
        alt=in_memory_file_content.name,
        file=in_memory_file_content,
        created_by=request.user,
    )
    return new_file


def delete_file(file_id):
    try:
        file = FileGallery.objects.get(id=file_id)
        file.delete()
        return True
    except:
        return False
