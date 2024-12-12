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
        
        signed_user=[]
        try:
            signed_user.append(User.objects.get(email=email).id)

        except User.DoesNotExist:
            signed_user.append("User Doesn't Exist")
        

        if signed_user[0]=="User Doesn't Exist":
            return Response({"message": "User does not exist. Please register the user first."}, 
                                status=status.HTTP_400_BAD_REQUEST)


        # Extract employee data from request
        employee_data = EmployeeHelper.extract_employee_data(request)
        employee_data['user'] = signed_user[0]

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

    def get(self, request, user_id=None):
        """Admin can retrieve any employee"""
        if user_id:
            try:
                employee = Employee.objects.get(user=user_id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """Admin can update any employee"""
        try:
            employee = Employee.objects.get(user=user_id)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update email if it's changed
        new_email = request.data.get("email", None)

        if not User.objects.filter(email=new_email).exists():
        # Check if the email is provided and if it's different from the current user's email
            if new_email and new_email != employee.user.user.email:
                # Update the user's email if it's different
                employee.user.user.email = new_email
                employee.user.user.save()  # Save the user after email update
        
        else:
            request.data["email"]=employee.user.user.email
       
    
      
        
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Admin can delete any employee"""
        try:
            employee = User.objects.get(user=user_id) 
            employee.delete()
            return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def get_profile(self,request):
        return EmployeeHelper.get_profile(request)
        
