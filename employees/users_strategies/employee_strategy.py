from rest_framework.response import Response
from rest_framework import status
from employees.users_strategies.user_strategy import UserStrategy
from employees.users_strategies.employee_helper import EmployeeHelper

# Strategy for Employee
class EmployeeStrategy(UserStrategy):
    def post(self, request):
        return Response({"detail": "Employees cannot create other employees."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, user_id=None):
        return Response({"detail": "Employees can only view their own profiles."}, status=status.HTTP_403_FORBIDDEN)
              

    def put(self, request, user_id):
        return Response({"detail": "Employees cannot update other employees."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id):
        return Response({"detail": "Employees cannot delete other employees."}, status=status.HTTP_403_FORBIDDEN)


    def get_profile(self,request):
        return EmployeeHelper.get_profile(request)
    
    def complete_account_data(self, request):
        return Response({"detail": "Employees Are Not Allowed to Complete their account without permission. "},
                         status=status.HTTP_403_FORBIDDEN)