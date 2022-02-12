from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'zarinpal'
router = DefaultRouter()

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
]
