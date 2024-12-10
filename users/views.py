# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserInfoSerializer
from .security.custom_jwt_auth import CustomJWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

class RegistrationView(APIView):
    """
    Handles user registration/signup process by creating a new User and UserInfo.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Parse the data from the request
            user_serializer = UserSerializer(data=request.data)
            
            if user_serializer.is_valid():
                if User.objects.filter(email=request.data["email"]).exists():
                    return Response({"email":["This e-mail already exists, Please Try Again"]},status=status.HTTP_400_BAD_REQUEST)
                user = user_serializer.save()

                # Now create the user info instance
                user_info_data = {
                    'user': user.id,
                    'role': request.data.get('role', 'Employee')  # Default to 'Employee'
                }
                user_info_serializer = UserInfoSerializer(data=user_info_data)

                if user_info_serializer.is_valid():
                    user_info_serializer.save()

                    return Response({'message': 'User successfully created!'}, status=status.HTTP_201_CREATED)
                else:
                    # If user info is not valid, delete the user
                    user.delete()
                    return Response(user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        



class LogOutView(APIView):
    """
    View to log out a user by blacklisting the refresh token.
    
    """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        """
        Handles POST requests to log out the user by blacklisting the refresh token.
        The refresh token is taken from the cookies and stored in the blacklist.
        """
        # Get the refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            # If no refresh token is found in cookies, raise an error
            raise AuthenticationFailed('No refresh token found in cookies.')

        try:
            # Retrieve the OutstandingToken instance using the refresh token
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)

            # Create a new BlacklistedToken instance using the OutstandingToken
            BlacklistedToken.objects.create(token=outstanding_token)

            # Return a success message after blacklisting the refresh token
            return Response({"message": "You have successfully logged out!"}, status=200)

        except ObjectDoesNotExist:
            # If the OutstandingToken instance does not exist, handle the error
            raise AuthenticationFailed('Refresh token does not exist in OutstandingToken.')

        except Exception as e:
            # Catch any other errors and return an error message
            raise AuthenticationFailed(f'message : error occurred while logging out process')



