from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
import users.models

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that extends JWTAuthentication to:
    - Extract and validate access and refresh tokens from cookies.
    - Check if the user is blacklisted by comparing the refresh token.
    - Attach the user's role to the request object.
    """
    def authenticate(self, request):
        try:
            # Retrieve access and refresh tokens from the request cookies
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')

            if access_token:
                # Decode and validate the access token using UntypedToken
                token = UntypedToken(access_token)
                user = self.get_user(token)  # Get the user associated with the token

                # Query the UserInfo model to retrieve the user's role based on the username
                user_info = users.models.UserInfo.objects.raw('''
                    SELECT u1.id, u1.role
                    FROM users_userinfo AS u1
                    JOIN auth_user AS u2 ON u1.user_id = u2.id
                    WHERE u2.username = %s
                ''', [str(user)])

                # If the role is found, attach it to the request object
                if user_info:
                    request.role = user_info[0].role

            else:
                # If no access token found, fallback to the default authentication mechanism
                user, token = super().authenticate(request)

            # Retrieve all blacklisted refresh tokens
            blacklisted_tokens = BlacklistedToken.objects.all()
            blacklisted_tokens_list = [t.token.token for t in blacklisted_tokens]

            # Check if the refresh token is blacklisted
            if str(refresh_token) in blacklisted_tokens_list:
                raise AuthenticationFailed('Invalid refresh token (blacklisted)', code='invalid_token')

            # Return the user and token as per normal JWT authentication
            return user, token

        except AuthenticationFailed as auth_error:
            # Handle any specific authentication failure exceptions
            raise AuthenticationFailed(f'Authentication failed: {str(auth_error)}')

        except Exception as e:
            # Catch any other unexpected errors and log them
            # print(f"Unexpected error in authentication: {e}")
            raise AuthenticationFailed('Authentication failed due to unexpected error.')

