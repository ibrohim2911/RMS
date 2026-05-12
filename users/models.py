import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom UserManager for User model."""
    
    def create_user(self, phone_number, name, password=None, **extra_fields):
        """Create and save a regular user."""
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if not name:
            raise ValueError("The Name field must be set")
        
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, name, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    role = models.ManyToManyField(Role, related_name='permissions')
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    pin = models.IntegerField(unique=True, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    c_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["name"]
    
    # Remove unnecessary fields
    username = None
    first_name = None
    last_name = None
    
    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    