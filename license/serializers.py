from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.License
        fields = '__all__'
        # depth = 1
