from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.path.startswith('/static/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
            if request.path == '/users/login/':
                response['Cache-Control'] += ', no-store'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '-1'
        return response

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
            
        public_paths = [
            '/users/login/',
            '/users/register/',
            '/',
            '/favicon.ico',
        ]
        
        access_token = request.COOKIES.get('access_token')
        
        if access_token and request.path in ['/users/login/', '/users/register/']:
            try:
                AccessToken(access_token)
                return redirect('posts:home')
            except (InvalidToken, TokenError):
                pass
        
        if request.path in public_paths:
            return self.get_response(request)
            
        if not access_token:
            return redirect('users:login')
            
        try:
            AccessToken(access_token)
        except (InvalidToken, TokenError):
            response = redirect('users:login')
            response.delete_cookie('access_token')
            return response
            
        return self.get_response(request)