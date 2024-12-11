from django.db import models
from companies.models import Company

class Department(models.Model):
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=255,unique=True)
    
    @property
    def num_of_employees(self):
        # Calculate the number of employees in this department
        return self.employees.count() 

    def __str__(self):
        return f"{self.dept_name} - {self.company.company}"



