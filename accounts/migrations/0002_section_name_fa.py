# Generated by Django 5.0.3 on 2024-05-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='name_fa',
            field=models.CharField(default=1, editable=False, max_length=255, verbose_name='نام فارسی'),
            preserve_default=False,
        ),
    ]
