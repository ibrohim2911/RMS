from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet, basename='menuitem')
router.register(r'menu-categories', views.MenuCategoryViewSet, basename='menucategory')
router.register(r'resources', views.ResourceViewSet, basename='resource')
router.register(r'menu-item-resources', views.MenuItemResourceViewSet, basename='menuitemresource')
router.register(r'inventory-categories', views.inventoryCategoryViewSet, basename='inventorycategory')
router.register(r'producers', views.ProducerViewSet, basename='producer')
router.register(r'resource-items', views.ResourceItemViewSet, basename='resourceitem')
urlpatterns = router.urls