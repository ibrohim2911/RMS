from decimal import Decimal

from django.db import models
from common.models import CommonModel
OrderStatusChoices = [
    ('open', 'Open'),
    ('preclosed', 'Pre-Closed'),
    ('closed', 'Closed'),
    ('paid', 'Paid'),
]

class OrderPayment(CommonModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)

class Order(CommonModel):
    table = models.ForeignKey('table.Table', on_delete=models.CASCADE, related_name='orders')
    waiter = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=OrderStatusChoices, default='open')    
class OrderItem(CommonModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('inventory.MenuItem', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orderer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordered_items')
    is_deleted = models.BooleanField(default=False)