# Generated by Django 5.0.6 on 2024-12-11 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_employee_user_alter_employee_designation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
    ]