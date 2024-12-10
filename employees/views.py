from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.security.custom_jwt_auth import CustomJWTAuthentication
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.exceptions import NotFound

class CreateEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the employee already exists with the same email or mobile number
        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')

        if Employee.objects.filter(email=email).exists():
            return Response({"detail": "Employee with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if Employee.objects.filter(mobile_number=mobile_number).exists():
            return Response({"detail": "Employee with this mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")
        
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            # Ensure department belongs to the same company as the employee
            department = serializer.validated_data.get('department', employee.department)
            company = serializer.validated_data.get('company', employee.company)

            if department.company != company:
                return Response({"detail": "Department must belong to the selected company."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")

        employee.delete()
        return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ListEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

