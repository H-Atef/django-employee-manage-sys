# Generated by Django 5.0.6 on 2024-12-10 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='company_name',
            new_name='company',
        ),
    ]