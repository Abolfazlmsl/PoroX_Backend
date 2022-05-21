from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'license'
router = DefaultRouter()

router.register('device', views.DeviceViewSet, 'license_url')
router.register('license', views.LicenseViewSet, 'device_url')

urlpatterns = [
    path('', include(router.urls)),
]
