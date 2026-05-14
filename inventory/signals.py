from django.db.models.signals import post_save
from . import models
from django.dispatch import receiver

@receiver(post_save, sender=models.MenuItem)
def change_menuitem_default(sender, instance, created, **kwargs):
    if created:
        if instance.printer is None:
            instance.printer = instance.category.default_printer
        if instance.order_status is None:
            instance.order_status = instance.category.default_status
