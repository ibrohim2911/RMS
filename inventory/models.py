from django.db import models
from common.models import CommonModel

class StorageLocation(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class inventoryCategory(CommonModel):
    name = models.CharField(max_length=255)

class Producer(CommonModel):
    name= models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

class Resource(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    category = models.ForeignKey(inventoryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="resources")

class ResourceItem(CommonModel):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="item")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name="item")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    extra_info = models.TextField(blank=True, null=True)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")

class MenuCategory(CommonModel):
    name = models.CharField(max_length=255)
    default_printer = models.ManyToManyField('hardware.Printer', blank=True, related_name='menu_categories')

class MenuItem(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
    printer = models.ManyToManyField('hardware.Printer', blank=True, related_name='menu_items')
    
class MenuItemResource(CommonModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="resources")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="menu_items")
    quantity = models.IntegerField()

