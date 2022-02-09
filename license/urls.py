from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'license'
router = DefaultRouter()

router.register('device', views.DeviceViewSet)
router.register('license', views.LicenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
