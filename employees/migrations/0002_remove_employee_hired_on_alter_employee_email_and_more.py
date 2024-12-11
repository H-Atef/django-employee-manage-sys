# Generated by Django 5.0.6 on 2024-12-11 04:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='hired_on',
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?20?\\d{11}$')]),
        ),
    ]
