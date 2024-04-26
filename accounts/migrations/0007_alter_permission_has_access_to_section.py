# Generated by Django 5.0.3 on 2024-04-26 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_permission_has_access_to_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='has_access_to_section',
            field=models.CharField(choices=[('user', 'کاربر'), ('permission', 'مجوز'), ('role', 'نقش'), ('ticket_admin', 'تیکت ادمین'), ('resource', 'منابع'), ('product', 'محصولات'), ('teaser_maker', 'تیزر ساز'), ('reseller_network', 'شبکه'), ('receiver', 'دریافت کننده'), ('advertise_content', 'محتوای تبلیغاتی'), ('forward_to_portal', 'انتقال دهنده'), ('communication_channel', 'کانال ارتباطی'), ('registrar', 'تخصیص دهنده'), ('automation', 'اتوماسیون'), ('automation_project', 'اتوماسیون - ساخت پروژه'), ('automation_task', 'اتوماسیون - ایجاد وظیفه'), ('automation_communicate', 'اتوماسیون - مکاتبات'), ('conversation', 'چت')], max_length=255, verbose_name='دسترسی به بخش'),
        ),
    ]
