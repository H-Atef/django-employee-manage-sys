from django.db import models
from companies.models import Company


class Department(models.Model):
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    num_of_employees = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    def save(self, *args, **kwargs):
        self.num_of_employees = self.employees.count()
        super().save(*args, **kwargs)

