import pytest

from core.models import Device, License
from django.urls import reverse


@pytest.mark.django_db
def test_core_create():
    device = Device.objects.create(deviceMac='11:22:33:44:55')
    license = License.objects.create(expired_on='2022-04-19')

    assert Device.objects.count() == 1
    assert device.deviceMac == '11:22:33:44:55'
    assert License.objects.count() == 1


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_device_request(api_client):
    Device.objects.create(deviceMac='11:22:33:44:55')
    url = reverse('license:device_url-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_license_request(api_client):
    license = License.objects.create(expired_on='2022-04-19')
    url = reverse('license:license_url-list')
    response = api_client.get(url)
    assert response.status_code == 401