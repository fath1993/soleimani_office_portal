# Generated by Django 5.0.3 on 2024-05-11 13:41

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gallery', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')),
                ('member_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_conversation_member_1', to=settings.AUTH_USER_MODEL, verbose_name='member 1')),
                ('member_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_conversation_member_2', to=settings.AUTH_USER_MODEL, verbose_name='member 2')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='private_conversation_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='بروز شده توسط')),
            ],
            options={
                'verbose_name': 'چت شخصی',
                'verbose_name_plural': 'چت های شخصی',
                'unique_together': {('member_1', 'member_2')},
            },
        ),
        migrations.CreateModel(
            name='ConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('attachments', models.ManyToManyField(blank=True, to='gallery.filegallery', verbose_name='ضمائم')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_conversation_message', to=settings.AUTH_USER_MODEL, verbose_name='ساخته شده توسط')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation_message', to='conversation.privateconversation', verbose_name='چت شخصی')),
            ],
            options={
                'verbose_name': 'پیام چت',
                'verbose_name_plural': 'پیام چت ها',
                'ordering': ['-created_at'],
            },
        ),
    ]
