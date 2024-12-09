from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            access_token = request.COOKIES.get('access_token')
            if access_token:
                token = UntypedToken(access_token)
                user = self.get_user(token)
            else:
                user, token = super().authenticate(request)

            blacklisted_tokens = BlacklistedToken.objects.all()
            blacklisted_tokens_iat = [int(t.token.created_at.timestamp()) for t in blacklisted_tokens]
            
            if 'iat' in token.payload and int(token.payload['iat']) in blacklisted_tokens_iat:
                raise AuthenticationFailed('Invalid token', code='invalid_token')

            return user, token
        except Exception as e:
            pass

 
           

