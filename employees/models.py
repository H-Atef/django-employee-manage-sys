from django.db import models
from companies.models import Company
from departments.models import Department
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
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    mobile_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?20?\d{11}$')])
    address = models.TextField()
    designation = models.CharField(max_length=255)
    hired_on = models.DateField(null=True, blank=True)
    days_employed = models.IntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):

        # Automatically calculate the number of days employed
        if self.hired_on:
            self.days_employed = (timezone.now().date() - self.hired_on).days
        
        # Ensure Department is related to the selected company
        if self.department.company != self.company:
            raise Exception("Department must belong to the selected company.")
        
        super().save(*args, **kwargs)
