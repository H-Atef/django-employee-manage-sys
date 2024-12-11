from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from employees.serializers import EmployeeSerializer
from employees.models import Employee
from employees.users_strategies.user_strategy import UserStrategy
from employees.users_strategies.employee_helper import EmployeeHelper
from datetime import date

class AdminStrategy(UserStrategy):

    def post(self, request):
        """Handles creating a new user and employee"""
        email = request.data.get("email")
        user_name = request.data.get("username", None)
        password = request.data.get("password", None)
        
        # Extract employee data from request
        employee_data = EmployeeHelper.extract_employee_data(request)

        # Check if the email already exists in Employee model
        if Employee.objects.filter(email=email).exists():
            return Response({"message": "Employee with this email already exists and their account is complete."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user already exists in the User model
        if EmployeeHelper.check_if_user_exists(email):
            return Response({"message": "User already exists. Please use the complete account data method if you need to update the data."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # If the user doesn't exist, create the user and employee
        return self.create_new_user_and_employee(user_name, password, email, employee_data, request)
    
    def create_new_user_and_employee(self, user_name, password, email, employee_data, request):
        """Create a new user and employee if the user does not exist"""
        user_data = {
            'username': user_name,
            'password': password,
            'email': email
        }

        # Create the user
        user, user_error = EmployeeHelper.create_user(user_data)
        if user_error:
            return Response(user_error, status=status.HTTP_400_BAD_REQUEST)

        # Create user info
        user_info, user_info_error = EmployeeHelper.create_user_info(user.id, request.data.get('role', 'Employee'))
        if user_info_error:
            user.delete()  # If user info creation fails, delete the user
            return Response(user_info_error, status=status.HTTP_400_BAD_REQUEST)
        
        employee_data['user'] = user.id

        # Create employee record
        employee, employee_error = EmployeeHelper.create_employee(employee_data)
        if employee_error:
            user.delete()  # If employee creation fails, delete the user
            return Response(employee_error, status=status.HTTP_400_BAD_REQUEST)

        return Response(employee, status=status.HTTP_201_CREATED)

    def complete_account_data(self, request):
        """Handle incomplete accounts data for existing users"""
        email = request.data.get("email")

        # Check if the email already exists in Employee model
        if Employee.objects.filter(email=email).exists():
            return Response({"message": "Employee with this email already exists and their account is complete."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists in Employee model
        if not Employee.objects.filter(email=email).exists():
            return Response({"message": "User does not exist. Please register the user first."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Extract employee data from request
        employee_data = EmployeeHelper.extract_employee_data(request)

        # Create or update employee with the incomplete data
        try:
            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Employee Update Process Failed! {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        """Admin can retrieve any employee"""
        if pk:
            try:
                employee = Employee.objects.get(pk=pk)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Admin can update any employee"""
        try:
            employee = Employee.objects.get(pk=pk)
            old_email = employee.email
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update email if it's changed
        new_email = request.data.get("email", None)
        if new_email and (old_email != new_email):
            user = EmployeeHelper.update_user_email(old_email, new_email)
            if not user:
                return Response({"detail": "User email not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Admin can delete any employee"""
        try:
            employee = User.objects.get(pk=pk)
            employee.delete()
            return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def get_profile(self,request):
        return EmployeeHelper.get_profile(request)
        
