from rest_framework import serializers
from .models import inventoryCategory, Producer, Resource, ResourceItem, StorageLocation, MenuCategory, MenuItem, MenuItemResource
class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = '__all__'
class inventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryCategory
        fields = '__all__'
class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
class ResourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = '__all__'
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
class MenuItemResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemResource
        fields = '__all__'


