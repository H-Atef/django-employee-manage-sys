from rest_framework.response import Response
from rest_framework import status
from employees.users_strategies.user_strategy import UserStrategy
from employees.serializers import EmployeeSerializer
from employees.models import Employee

# Strategy for Manager
class ManagerStrategy(UserStrategy):
    def post(self, request):
        # Managers can create employees only within their department
        department = request.data.get('department')
        user_department = request.user.department.id  # Assuming request.user is related to a department

        if department != user_department:
            return Response({"detail": "Manager can only create employees within their department."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        # Manager can view employees from their own department
        if pk:
            try:
                employee = Employee.objects.get(pk=pk, department=request.user.department)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        employees = Employee.objects.filter(department=request.user.department)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Manager can update employees only in their own department
        try:
            employee = Employee.objects.get(pk=pk, department=request.user.department)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Manager can delete only employees in their own department
        try:
            employee = Employee.objects.get(pk=pk, department=request.user.department)
            employee.delete()
            return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def get_profile(self, request, pk):
        pass
