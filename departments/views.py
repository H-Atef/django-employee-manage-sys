from . import serializers, models
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from users.security.custom_jwt_auth import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework import mixins

# Function accessible by authenticated users only
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated]) 
def view_all_departments(request):
    """
    Get a list of all departments.
    This view is accessible to authenticated users only.
    """
    # Fetch all departments
    departments = models.Department.objects.all()

    # Serialize the data
    serialized_departments = serializers.DepartmentSerializer(departments, many=True)

    # Return the serialized data with HTTP 200 OK status
    return Response(serialized_departments.data, status=status.HTTP_200_OK)

# Function accessible only by authenticated users
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])  
def view_department_by_id(request, dept_id):
    """
    Get a specific department by ID.
    This view is accessible to authenticated users (manager, admin, and employee).
    If the department doesn't exist, return a 404 error.
    """
    try:
        # Fetch the department by id
        department = models.Department.objects.get(id=dept_id)

        # Serialize the data
        serialized_department = serializers.DepartmentSerializer(department)

        # Return the serialized data with HTTP 200 OK status
        return Response(serialized_department.data, status=status.HTTP_200_OK)
    
    except models.Department.DoesNotExist:
        # If department does not exist, return a 404 error with message
        raise NotFound(detail="Department not found", code=status.HTTP_404_NOT_FOUND)

# Department ViewSet for CRUD operations
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    authentication_classes=[CustomJWTAuthentication]

    # Set permission to restrict access to Admin only
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only admins can create, update, or delete
        return [IsAuthenticated()]  # Other actions (e.g., list, retrieve) are accessible to authenticated users
    
