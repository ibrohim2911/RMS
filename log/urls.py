from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'logs', views.LogViewSet, basename='logentry')
urlpatterns = router.urls