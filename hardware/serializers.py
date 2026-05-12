from rest_framework import serializers
from .models import Printer, CashierPrinter, PrinterJob
class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'

class CashierPrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashierPrinter
        fields = '__all__'

class PrinterJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterJob
        fields = '__all__'