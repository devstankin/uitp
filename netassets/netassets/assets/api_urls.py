from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'network-devices', views.NetworkDeviceViewSet)
router.register(r'switches', views.SwitchViewSet)
router.register(r'computers', views.ComputerViewSet)
router.register(r'printers', views.PrinterViewSet)
router.register(r'routers', views.RouterViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 