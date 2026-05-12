from rest_framework import viewsets
from .models import Table, Reservation, Location
from .serializers import TableSerializer, ReservationSerializer, LocationSerializer
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('name')
    serializer_class = TableSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_tables'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_tables'
        return super().get_permissions()
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('-time')
    serializer_class = ReservationSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_reservations'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_reservations'
        return super().get_permissions()
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_locations'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_locations'
        return super().get_permissions()