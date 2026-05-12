from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'printers', views.PrinterViewSet, basename='printer')
router.register(r'printer-jobs', views.PrinterJobViewSet, basename='printerjob')
router.register(r'cashier-printers', views.CashierPrinterViewSet, basename='cashierprinter')
urlpatterns = router.urls