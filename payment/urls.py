from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment import views

app_name = 'payment'
router = DefaultRouter()

urlpatterns = [
    path('payment', views.payment_start, name='payment_start'),
    path('payment/return', views.payment_return, name='payment_return'),
    path('payment/check/<pk>', views.payment_check, name='payment_check'),
    path('requirement', views.requirement, name='requirement'),
    path('about-me', views.about_me, name='about_me'),
]
