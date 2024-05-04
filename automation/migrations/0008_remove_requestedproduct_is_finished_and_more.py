# Generated by Django 5.0.3 on 2024-05-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0007_remove_requestedproductprocessing_reports_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestedproduct',
            name='is_finished',
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='is_processed',
            field=models.BooleanField(default=False, verbose_name='پردازش شده'),
        ),
        migrations.AlterField(
            model_name='requestedproductprocessing',
            name='delivery_status',
            field=models.CharField(choices=[('processing', 'در حال پردازش'), ('delivered', 'تحویل شده به مشتری'), ('canceled', 'کنسل شده')], default='processing', max_length=255, verbose_name='وضعیت ارسال محصول درخواستی'),
        ),
    ]
