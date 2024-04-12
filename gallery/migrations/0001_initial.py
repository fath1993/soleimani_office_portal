# Generated by Django 5.0.3 on 2024-04-08 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.CharField(max_length=255, verbose_name='متن جایگزین فایل')),
                ('file', models.FileField(blank=True, null=True, upload_to='gallery/', verbose_name='فایل')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('created_by', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط')),
            ],
            options={
                'verbose_name': 'فایل',
                'verbose_name_plural': 'فایل ها',
                'ordering': ['-created_at'],
            },
        ),
    ]
