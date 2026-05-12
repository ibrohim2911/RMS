from common.models import CommonModel
from django.db import models

class Location(CommonModel):
    name = models.CharField(max_length=255)
    default_tax = models.DecimalField(max_digits=5, decimal_places=2)
class Table(CommonModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tables')
    capacity = models.IntegerField()
    availability = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
class Reservation(CommonModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    size = models.IntegerField()
    contact = models.CharField(max_length=255)
    extra_info = models.TextField(blank=True, null=True)
