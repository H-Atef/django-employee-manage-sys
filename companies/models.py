from django.db import models

class Company(models.Model):
    company = models.CharField(max_length=255,unique=True)

    @property
    def num_of_departments(self):
        # This computes the number of departments associated with this company
        return self.departments.count()

    @property
    def num_of_employess(self):
        # This computes the total number of employees across all departments
        return sum(department.num_of_employees for department in self.departments.all())
    
    

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
