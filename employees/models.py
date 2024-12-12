from django.db import models
from companies.models import Company
from departments.models import Department
from users.models import UserInfo
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone


STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('On Leave', 'On Leave'),
    ('Terminated', 'Terminated'),
]



class Employee(models.Model):
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    user=models.OneToOneField(UserInfo,related_name='employees', on_delete=models.CASCADE)
    email = models.EmailField(validators=[EmailValidator()],unique=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,default="Active")
    name = models.CharField(max_length=255,default="-")
    mobile_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?20?\d{11}$')],unique=True)
    address = models.TextField()
    designation = models.CharField(max_length=255,default="-")
    hired_on = models.DateField(null=True, blank=True)
    

    @property
    def days_employed(self):  
        # Automatically calculate the number of days employed
        if self.hired_on:
            return f"{(timezone.now().date() - self.hired_on).days} Days"
        else:
            return "0 Days"


    def save(self, *args, **kwargs):
        
        # Ensure Department is related to the selected company
        if self.department.company != self.company:
            raise Exception("Department must belong to the selected company.")
        
        self.email=self.user.user.email
        
        super().save(*args, **kwargs)
