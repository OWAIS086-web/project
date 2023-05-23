from rest_framework.generics import *
from rest_framework.response import Response

from .serializers import *


class OneSignalDeviceListAPIView(ListCreateAPIView):
    serializer_class = OneSignalDeviceSerializer
    queryset = OneSignalDevice.objects.none()

    def get_queryset(self):
        return OneSignalDevice.objects.filter(user=self.request.user)


class OneSignalDeviceDetailAPIView(ListCreateAPIView):
    serializer_class = OneSignalDeviceDetailSerializer
    queryset = OneSignalDevice.objects.none()

    def get_queryset(self):
        return OneSignalDevice.objects.filter(user=self.request.user)\


    def create(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')
        devices = OneSignalDevice.objects.filter(device_id=device_id, user=self.request.user)
        if devices.exists():
            return Response({
                'detail': 'This device is already added in your account.'
            }, status=400)
        return super(OneSignalDeviceDetailAPIView, self).create(request, *args, **kwargs)
