from fcm_django.api.rest_framework import DeviceSerializerMixin
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


class FCMDeviceSerializerInLogin(serializers.ModelSerializer):
    class Meta(DeviceSerializerMixin.Meta):
        model = FCMDevice

        extra_kwargs = {"id": {"read_only": True, "required": False}}
        extra_kwargs.update(DeviceSerializerMixin.Meta.extra_kwargs)


class AccountAuthTokenSerializer(AuthTokenSerializer):
    device = FCMDeviceSerializerInLogin(write_only=True, required=False)
