from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'reservations', views.ReservationViewSet, basename='reservation')
router.register(r'locations', views.LocationViewSet, basename='location')
urlpatterns = router.urls
