from django.contrib import admin
from .models import Printer, CashierPrinter, PrinterJob
admin.site.register(Printer)
admin.site.register(CashierPrinter)
admin.site.register(PrinterJob)
