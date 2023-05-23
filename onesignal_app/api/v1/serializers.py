from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from onesignal_app.models import *


class OneSignalDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneSignalDevice
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class OneSignalDeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneSignalDevice
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'device_id': {
                'read_only': True
            }
        }
