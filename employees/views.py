from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.security.custom_jwt_auth import CustomJWTAuthentication
from employees.permissions.role_context import RoleContext

class CreateEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.post(request)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
        
class CompleteAccountEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.complete_account_data(request)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

class RetrieveEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, user_id=None):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.get(request, user_id)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

class UpdateEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def put(self, request, user_id):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.put(request, user_id)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

class DeleteEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def delete(self, request, user_id):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.delete(request, user_id)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

class ListEmployeeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.get(request)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
        
class EmployeeProfileAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user_role = request.user.userinfo.role
        role_context = RoleContext(user_role)
        strategy = role_context.get_strategy()

        if strategy:
            return strategy.get_profile(request)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
