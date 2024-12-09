from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import User




class UserInfo(models.Model):
    role_choices = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=role_choices, default='Employee')

    class Meta:
        verbose_name="User Info"
        verbose_name_plural="Users Info"
