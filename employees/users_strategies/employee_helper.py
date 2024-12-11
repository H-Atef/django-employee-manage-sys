from django.contrib.auth.models import User
from employees.models import Employee
from users.serializers import UserInfoSerializer, UserSerializer
from employees.serializers import EmployeeSerializer
from datetime import date
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status

class EmployeeHelper:

    @staticmethod
    def extract_employee_data(request):
        """Extract employee-related data from request"""
        employee_fields = [
            'company', 'department', 'status', 'name', 'email',
            'mobile_number', 'address', 'designation', 'hired_on'
        ]
        
        # Create a dictionary from request.data using the model fields
        employee_data = {field: request.data.get(field,None) for field in employee_fields}
        
        # If 'hired_on' is not in request data, set it to today's date
        employee_data['hired_on'] = request.data.get('hired_on', date.today())
        employee_data['status'] = employee_data.get('status', 'Active') 
        
        
        return employee_data

    @staticmethod
    def create_employee(employee_data):
        """Create the employee record"""
        try:
            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data,None
            else:
                return None, serializer.errors
        except Exception as e:
            return None, {"error": f"Employee Creation Process Failed! {e}"}

    @staticmethod
    def create_user(user_data):
        """Create the user for the employee"""
        try:
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                return user, None
            else:
                return None, user_serializer.errors
        except Exception as e:
            return None, {"error": f"User Creation Process Failed! {e}"}

    @staticmethod
    def create_user_info(user_id, role):
        """Create the user info record"""
        try:
            user_info_data = {
                'user': user_id,
                'role': role
            }
            user_info_serializer = UserInfoSerializer(data=user_info_data)
            if user_info_serializer.is_valid():
                user_info_serializer.save()
                return 0,None
            else:
                return None,user_info_serializer.errors
        except Exception as e:
            return {"error": f"User Info Creation Process Failed! {e}"}

    
    @staticmethod
    def check_if_user_exists(email):
        """Check if a user with the given email exists"""
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_profile(request):
        try:
            # Run the raw query and get the Employee objects
            profile_info = Employee.objects.raw("""
                SELECT *
                FROM employees_employee e
                INNER JOIN users_userinfo uinfo ON e.user_id = uinfo.user_id
                WHERE uinfo.user_id = %s
            """, [request.user.id])

            if profile_info:

                # Convert the result to a dictionary
                employee=profile_info[0]
                employee_dict = {
                        'id': employee.id,
                        'company': employee.company.id if employee.company else None,
                        'department': employee.department.id if employee.department else None,
                        'status': employee.status,
                        'name': employee.name,
                        'mobile_number': employee.mobile_number,
                        'address': employee.address,
                        'designation': employee.designation,
                        'hired_on': employee.hired_on,
                        'days_employed': f"{(timezone.now().date() - employee.hired_on).days} Days",
                        'email': request.user.email, 
                        'role': employee.role   
                    }
                
                return Response(employee_dict, status=status.HTTP_200_OK)
            
           
            profile_data = {
                    'id': request.user.id,
                    'email': request.user.email, 
                    'role': request.user.userinfo.role  
                }
            
           
            return Response(profile_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
  