from . import models
from order.models import Order, OrderItem
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.middleware import get_current_user
@receiver(post_save, sender=Order)
def create_p_job_for_cashier_printer(sender, instance, created, **kwargs):
    if instance.status == 'pre-closed' or instance.status == 'closed':
        cashier = get_current_user()
        cashier_printers = models.CashierPrinter.objects.filter(cashier=cashier)
        for cp in cashier_printers:
            for printer in cp.printer.all():
                models.PrinterJob.objects.create(
                    printer=printer,
                    payload=f"Order #{instance.id} - Total: {instance.total_amount}"
                )
@receiver(post_save, sender=OrderItem)
def create_printer_job_for_order_item(sender, instance, created, **kwargs):
    if created:
        printer = instance.menu_item.printer
        models.PrinterJob.objects.create(printer=printer,payload=f"{instance.menu_item.name} price: {instance.menu_item.price}")
