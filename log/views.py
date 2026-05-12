from rest_framework import viewsets
from .models import Log
from .serializers import LogSerializer
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_logs'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_logs'
        return super().get_permissions()