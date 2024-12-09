class SetTokenInHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response is from TokenObtainPairView
        if request.path == 'login/' and response.status_code == 200:
            # Extract the token from the response content
            token = response.data.get('access', None)
            #refresh_token = response.data.get('refresh', None)
            
            if token:
                
                response.set_cookie('access_token', token,httponly=True) 
                #response.set_cookie('refresh_token', refresh_token,httponly=True) 
        return response