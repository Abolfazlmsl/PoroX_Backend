from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'products'
router = DefaultRouter()

urlpatterns = [
    path('', views.main_products, name='main_products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]
