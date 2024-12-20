# Generated by Django 5.0.6 on 2024-12-11 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_remove_employee_user_employee_email'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.userinfo'),
            preserve_default=False,
        ),
    ]
