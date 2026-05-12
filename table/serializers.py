from rest_framework import serializers
from .models import Table, Reservation, Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
class TableSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    class Meta:
        model = Table
        fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'