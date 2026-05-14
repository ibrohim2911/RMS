from django.contrib import admin
from .models import MenuCategory, MenuItem, Resource, MenuItemResource, inventoryCategory, Producer, ResourceItem, StorageLocation, OrderStatus
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Resource)
admin.site.register(MenuItemResource)
admin.site.register(inventoryCategory)
admin.site.register(Producer)
admin.site.register(ResourceItem)
admin.site.register(StorageLocation)
admin.site.register(OrderStatus)