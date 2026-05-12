from .models import User, Role, Permission
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'slug']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'slug']
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permissions = PermissionSerializer(source='role.permissions', many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'password', 'role', 'permissions', 'is_active']
    
    def create(self, validated_data):
        """Create user with properly hashed password."""
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data, password=password)
        return user
    
    def update(self, instance, validated_data):
        """Update user, hashing password if provided."""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance