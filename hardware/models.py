from django.db import models
from common.models import CommonModel
class Printer(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    
class CashierPrinter(CommonModel):
    printer = models.ManyToManyField(Printer, blank=True, related_name='cashier_printers')
    cashier = models.ManyToManyField('users.User', blank=True, related_name='cashier_printers')
class PrinterJob(CommonModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('printing', 'Printing'),
        ('printed', 'Printed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payload = models.TextField() # Stores the actual text to print
    error_message = models.TextField(blank=True, null=True)