# Generated by Django 5.0.3 on 2024-05-04 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_usernotification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usernotification',
            options={'verbose_name': 'اطلاعیه کاربر', 'verbose_name_plural': 'اطلاعیه های کاربران'},
        ),
    ]
