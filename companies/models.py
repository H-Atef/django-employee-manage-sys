from django.db import models

class Company(models.Model):
    company_name=models.CharField(max_length=255)
    num_of_departments=models.IntegerField(default=0)
    num_of_employess=models.IntegerField(default=0)


    def save(self,*args,**kwargs):
        self.num_of_departments=self.departments.count()
        super().save(*args, **kwargs)

    


    class Meta:
        verbose_name="Company"
        verbose_name_plural="Companies"