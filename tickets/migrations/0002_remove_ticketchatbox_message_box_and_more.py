# Generated by Django 5.0.3 on 2024-04-14 13:23

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('tickets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketchatbox',
            name='message_box',
        ),
        migrations.RemoveField(
            model_name='ticketchatbox',
            name='user',
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ایجاد شده', 'ایجاد شده'), ('در حال بررسی', 'در حال بررسی'), ('پاسخ ادمین', 'پاسخ ادمین'), ('بسته شده', 'بسته شده'), ('پاسخ کاربر', 'پاسخ کاربر')], default='pending', max_length=255, verbose_name='وضعیت تیکت')),
                ('title', models.CharField(blank=True, max_length=512, null=True, verbose_name='عنوان تیکت')),
                ('has_seen_by_user', models.BooleanField(default=False, verbose_name='دیده شده توسط کاربر')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')),
                ('belong_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_belong_to', to=settings.AUTH_USER_MODEL, verbose_name='متعلق به')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_created_by', to=settings.AUTH_USER_MODEL, verbose_name='ساخته شده توسط')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='بروز شده توسط')),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت ها',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('attachments', models.ManyToManyField(blank=True, to='gallery.filegallery', verbose_name='ضمائم')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_message', to=settings.AUTH_USER_MODEL, verbose_name='ساخته شده توسط')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_message', to='tickets.ticket', verbose_name='تیکت')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='MessageContent',
        ),
        migrations.DeleteModel(
            name='TicketChatBox',
        ),
    ]
