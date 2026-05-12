from django.shortcuts import render
from .models import User, Role, Permission
from .serializer import UserSerializer, RoleSerializer, PermissionSerializer
from rest_framework import viewsets
from .permissions import HasDynamicPermission
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasDynamicPermission]
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_users'
        elif self.action == ['list', 'retrieve']:
            self.required_permission = 'view_users'
        return super().get_permissions()
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasDynamicPermission]
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_roles'
        elif self.action == ['list', 'retrieve']:
            self.required_permission = 'view_roles'
        return super().get_permissions()
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [HasDynamicPermission]
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_permissions'
        elif self.action == ['list', 'retrieve']:
            self.required_permission = 'view_permissions'
        return super().get_permissions()