from django.contrib.auth.backends import ModelBackend
from .models import User


class PhoneNumberBackend(ModelBackend):
    """
    Custom authentication backend that uses phone_number instead of username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate using phone_number and password.
        """
        try:
            user = User.objects.get(phone_number=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
