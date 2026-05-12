from rest_framework import viewsets
from .models import Printer, CashierPrinter, PrinterJob
from .serializers import PrinterSerializer, CashierPrinterSerializer, PrinterJobSerializer
class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_printers'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_printers'
        return super().get_permissions()
class CashierPrinterViewSet(viewsets.ModelViewSet):
    queryset = CashierPrinter.objects.all()
    serializer_class = CashierPrinterSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_cashier_printers'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_cashier_printers'
        return super().get_permissions()
class PrinterJobViewSet(viewsets.ModelViewSet):
    queryset = PrinterJob.objects.all()
    serializer_class = PrinterJobSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_printer_jobs'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_printer_jobs'
        return super().get_permissions()