from django.db import models
from django.contrib.auth.models import User




class UserInfo(models.Model):
    role_choices = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=role_choices, default='Employee')


    def save(self, *args, **kwargs):
        # Check if the role is 'Admin'
        if self.role == 'Admin':
            # Grant superuser permissions to the associated user
            self.user.is_superuser = True
            self.user.is_staff = True  # If you want to grant staff access as well
        else:
            # Revoke superuser permissions if the role is not 'Admin'
            self.user.is_superuser = False
            self.user.is_staff = False  # Remove staff access for non-admins

        # Save the User first, so that the is_superuser flag is updated
        self.user.save()

        # Now save the UserInfo object itself
        super().save(*args, **kwargs)



    def __str__(self):
        return f"User Info {self.id}"



    class Meta:
        verbose_name="User Info"
        verbose_name_plural="Users Info"
