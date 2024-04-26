from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels

from gallery.models import FileGallery


class PrivateConversation(models.Model):
    member_1 = models.ForeignKey(User, related_name='private_conversation_member_1', on_delete=models.CASCADE,
                                 null=False,
                                 blank=False, editable=True, verbose_name='member 1')
    member_2 = models.ForeignKey(User, related_name='private_conversation_member_2', on_delete=models.CASCADE,
                                 null=False,
                                 blank=False, editable=True, verbose_name='member 2')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    updated_by = models.ForeignKey(User, related_name='private_conversation_updated_by', on_delete=models.CASCADE,
                                   null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'member_1: {self.member_1.username} | member_2: {self.member_2.username}'

    class Meta:
        unique_together = ('member_1', 'member_2')
        verbose_name = 'چت شخصی'
        verbose_name_plural = 'چت های شخصی'


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(PrivateConversation, related_name='conversation_message', on_delete=models.CASCADE,
                                     null=False, blank=False,
                                     verbose_name='چت شخصی')
    content = models.TextField(null=False, blank=False, verbose_name='محتوا')
    attachments = models.ManyToManyField(FileGallery, blank=True, verbose_name='ضمائم')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_conversation_message', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ساخته شده توسط')

    def __str__(self):
        return f'conversation_id: {self.conversation.id} | message_id: {self.id}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام چت ها'
