import pytest

from products.models import Product
from django.urls import reverse


@pytest.mark.django_db
def test_product_create():
    product = Product.objects.create(price='20000', deviceUsers='2', time='90')

    assert Product.objects.count() == 1
    assert product.price == '20000'
    assert product.deviceUsers == '2'
    assert product.time == '90'


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_product_request(api_client):
    Product.objects.create(id='1', price='20000', deviceUsers='2', time='90')
    url = reverse('products:product_detail', kwargs={'product_id': 1})
    response = api_client.get(url)
    assert response.status_code == 200
