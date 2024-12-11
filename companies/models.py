from django.db import models
# from django.db import connection

class Company(models.Model):
    company = models.CharField(max_length=255,unique=True)

    @property
    def num_of_departments(self):
        # This computes the number of departments associated with this company
        return self.departments.count()

    @property
    def num_of_employess(self):

        # # Clear the previous queries from the connection object
        # connection.queries.clear()

        departments = self.departments.prefetch_related('employees')
        total_employees = sum(department.employees.count() for department in departments.all())

        # # Print the queries executed during this method call
        # print("SQL Queries:")
        # for query in connection.queries:
        #     print(query['sql'])

        return total_employees
    

    
    

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
