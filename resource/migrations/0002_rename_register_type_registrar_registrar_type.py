# Generated by Django 5.0.3 on 2024-06-02 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrar',
            old_name='register_type',
            new_name='registrar_type',
        ),
    ]
