from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Table, Reservation, Location
@receiver(post_save, sender=Table)
def table_tax_set_if_null(sender, instance, created, **kwargs):
    if created and instance.tax is None:
        instance.tax = instance.location.tax
        instance.save()
