from rest_framework import viewsets
from .models import MenuCategory, MenuItem, Resource, MenuItemResource, inventoryCategory, Producer, ResourceItem, StorageLocation
from .serializers import MenuCategorySerializer, MenuItemSerializer, ResourceSerializer, MenuItemResourceSerializer, inventoryCategorySerializer, ProducerSerializer, ResourceItemSerializer, StorageLocationSerializer
class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_menu_categories'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_menu_categories'
        return super().get_permissions()
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_menu_items'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_menu_items'
        return super().get_permissions()
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_resources'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_resources'
        return super().get_permissions()
class MenuItemResourceViewSet(viewsets.ModelViewSet):
    queryset = MenuItemResource.objects.all()
    serializer_class = MenuItemResourceSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_menu_item_resources'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_menu_item_resources'
        return super().get_permissions()
class inventoryCategoryViewSet(viewsets.ModelViewSet):
    queryset = inventoryCategory.objects.all()
    serializer_class = inventoryCategorySerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_inventory_categories'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_inventory_categories'
        return super().get_permissions()
class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_producers'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_producers'
        return super().get_permissions()
class ResourceItemViewSet(viewsets.ModelViewSet):
    queryset = ResourceItem.objects.all()
    serializer_class = ResourceItemSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_resource_items'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_resource_items'
        return super().get_permissions()
class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_storage_locations'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_storage_locations'
        return super().get_permissions()
    