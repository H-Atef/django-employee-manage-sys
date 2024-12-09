# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import UserInfo
from .serializers import UserSerializer, UserInfoSerializer

class SignUpView(APIView):
    """
    Handles user signup by creating a new User and UserInfo.
    """

    def post(self, request):
        try:
            # Parse the data from the request
            user_serializer = UserSerializer(data=request.data)
            
            if user_serializer.is_valid():
                # Save the user first
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
            return Response({"error":f"{e}"})
