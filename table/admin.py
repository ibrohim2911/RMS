from django.contrib import admin
from .models import Table, Reservation, Location
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Location)