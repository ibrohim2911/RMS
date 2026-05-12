from decimal import Decimal

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from table.models import Table, Reservation, Location
from .models import Order, OrderItem, OrderPayment
@receiver(post_save, sender=OrderItem)
def update_payment_on_order_item_change(sender, instance, created, **kwargs):
    order = instance.order
    table = instance.order.table
    total_amount = sum(item.price * item.quantity for item in order.items.filter(is_deleted=False))
    order.raw_price = total_amount
    order.price = total_amount * Decimal(str(table.tax))
    order.save()
@receiver(post_delete, sender=OrderItem)
def update_payment_on_order_item_delete(sender, instance, **kwargs):
    order = instance.order
    table = instance.order.table
    total_amount = sum(item.price * item.quantity for item in order.items.filter(is_deleted=False))
    order.raw_price = total_amount
    order.price = total_amount * Decimal(str(table.tax))
    order.save()
