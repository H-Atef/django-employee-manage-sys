from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from users.security.custom_jwt_auth import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework import viewsets
from . import models, serializers

# Function accessible by all users 
@api_view(['GET'])
@permission_classes([AllowAny]) 
def view_all_companies(request):
    """
    Get a list of all companies.
    This view is accessible to all users.
    """
    # Fetch all companies
    companies = models.Company.objects.all()

    # Serialize the data
    serialized_companies = serializers.CompanySerializer(companies, many=True)

    # Return the serialized data with HTTP 200 OK status
    return Response(serialized_companies.data, status=status.HTTP_200_OK)

# Function accessible only by authenticated users (manager, admin, employee)
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def view_company_by_id(request, company_id):
    """
    Get a specific company by ID.
    This view is accessible to authenticated users (manager, admin, and employee).
    If the company doesn't exist, return a 404 error.
    """
    try:
        # Fetch the company by id
        company = models.Company.objects.get(id=company_id)

        # Serialize the data
        serialized_company = serializers.CompanySerializer(company)

        # Return the serialized data with HTTP 200 OK status
        return Response(serialized_company.data, status=status.HTTP_200_OK)
    
    except models.Company.DoesNotExist:
        # If company does not exist, return a 404 error with message
        raise NotFound(detail="Company not found", code=status.HTTP_404_NOT_FOUND)
    


# ViewSet for Company CRUD operations, accessible by admins and managers only
class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing company instances.
    Accessible to Admin and Manager roles only.
    """
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    authentication_classes=[CustomJWTAuthentication]

    # Set permission to restrict access to Admin only
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only admins can create, update, or delete
        return [IsAuthenticated()]  # Other actions (e.g., list, retrieve) are accessible to authenticated users
    
    
