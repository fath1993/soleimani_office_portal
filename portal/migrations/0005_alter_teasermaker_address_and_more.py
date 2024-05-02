# Generated by Django 5.0.3 on 2024-05-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_advertisecontent_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teasermaker',
            name='address',
            field=models.CharField(max_length=2000, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='teasermaker',
            name='content_type',
            field=models.CharField(choices=[('صوتی', 'صوتی'), ('تصویری', 'تصویری'), ('ویدیویی', 'ویدیویی'), ('متنی', 'متنی'), ('تلفیقی', 'تلفیقی'), ('اینستاگرامی', 'اینستاگرامی')], default='صوتی', max_length=255, verbose_name='نوع محتوا'),
        ),
    ]
