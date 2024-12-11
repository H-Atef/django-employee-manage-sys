from rest_framework.response import Response
from rest_framework import status
from employees.users_strategies.user_strategy import UserStrategy
from employees.serializers import EmployeeSerializer
from employees.models import Employee
from django.contrib.auth.models import User
from employees.users_strategies.employee_helper import EmployeeHelper

# Strategy for Manager
class ManagerStrategy(UserStrategy):
    def post(self, request):
        """Handles creating a new user and employee"""
        email = request.data.get("email")
        user_name = request.data.get("username", None)
        password = request.data.get("password", None)

        # Ensure the manager is only managing employees of the same company
        company = request.user.userinfo.company  # Assuming the manager's company is available in userinfo
        
        # Extract employee data from request
        employee_data = EmployeeHelper.extract_employee_data(request)
        
        # Validate that the employee is being assigned to the correct company
        if int(employee_data.get("company")) != company.id:
            return Response({"message": "You can only create employees for your assigned company."}, 
                            status=status.HTTP_400_BAD_REQUEST)

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



    def get(self, request, user_id=None):
        """Manager can retrieve employees from the same company."""
        try:
            # Attempt to get the employee record for the manager (user making the request)
            m_company = Employee.objects.get(user=request.user.id)
            company = m_company.company  # Get the company of the manager
            
        except Employee.DoesNotExist:
            # If the manager's employee record is not found, return an error
            return Response(
                {"detail": "Your account is incomplete or you are not assigned to a company."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If `user_id` is provided, attempt to retrieve a specific employee
        if user_id:
            try:
                # Get the employee by user_id
                employee = Employee.objects.get(user=user_id)
                
                # Check if the employee belongs to the same company as the manager
                if employee.company != company:
                    return Response(
                        {"message": "You can only access employees from your assigned company."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Serialize the employee data
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Employee.DoesNotExist:
                return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        # If no user_id is provided, return all employees from the same company
        employees = Employee.objects.filter(company=company)  # Only employees from the same company
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, user_id):
        """Manager can update employees from the same company, but not other managers"""
        try:
            # Get the manager's employee record to confirm they exist and have a valid company
            manager_employee = Employee.objects.get(user=request.user.id)

            # Get the manager's company from the employee record
            company = manager_employee.company

        except Employee.DoesNotExist:
            # If the manager does not exist or is incomplete
            return Response({"message": "Manager account is incomplete or does not exist."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the employee record to be updated
            employee = Employee.objects.get(user=user_id)
            
            # Ensure the employee belongs to the same company as the manager
            if employee.company != company:
                return Response({"message": "You can only update employees from your assigned company."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            
            
            # Prevent a manager from updating another manager's account
            if employee.user.role == "Manager" and request.user.id!=user_id:
                return Response({"message": "You cannot update another manager's account."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Get the current email and check if the new email is different
            old_email = employee.user.user.email
            new_email = request.data.get("email", None)
            
            # Check if the new email is different and update the email if necessary
            if new_email and new_email != old_email:
                if not User.objects.filter(email=new_email).exists():
                    # Update the user's email if it's different and not already in use
                    employee.user.user.email = new_email
                    employee.user.user.save()  # Save the updated email
                else:
                    return Response({"message": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Proceed to update the employee's data using the serializer
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Save the updated employee data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

    

    def delete(self, request, user_id):
        """Manager can delete employees from the same company, but not other managers or themselves."""
        
        try:
            # Get the manager's employee record to confirm they exist and have a valid company
            manager_employee = Employee.objects.get(user=request.user.id)

            # Get the manager's company from the employee record
            company = manager_employee.company

        except Employee.DoesNotExist:
            # If the manager does not exist or is incomplete
            return Response({"message": "Manager account is incomplete or does not exist."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the employee record by user_id
            employee = Employee.objects.get(user=user_id)
            
            # Ensure the employee belongs to the same company as the manager
            if employee.company != company:
                return Response({"message": "You can only delete employees from your assigned company."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure that the manager cannot delete other managers or themselves
            if employee.user.role == "Manager":
                if user_id == request.user.id:
                    return Response({"message": "You cannot delete yourself."}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "You cannot delete another manager."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Proceed with deletion if all conditions are met
            employee.delete()
            employee.user.user.delete()
            return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)


    def get_profile(self, request):
        """Manager can see their profile with employees related to the company"""
        return EmployeeHelper.get_profile(request)
