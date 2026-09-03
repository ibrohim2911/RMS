from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from common.models import Restaurant
from django.contrib.auth.models import AnonymousUser

class BranchAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        api_key = auth_header.split(' ')[1]
        try:
            restaurant = Restaurant.objects.get(api_key=api_key)
        except Restaurant.DoesNotExist:
            raise AuthenticationFailed('Invalid Branch API Key')
            
        return (AnonymousUser(), restaurant)
