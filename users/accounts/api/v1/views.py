from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .auth_serializers import AccountAuthTokenSerializer
from .serializers import *


class AccountTokenLoginAPIView(CreateAPIView):
    # serializer_class = AuthTokenSerializer
    serializer_class = AccountAuthTokenSerializer
    queryset = Token.objects.none()
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        fcm_device = serializer.validated_data.get('device', None)
        if fcm_device:
            from fcm_django.api.rest_framework import FCMDeviceSerializer
            from fcm_django.models import FCMDevice
            devices = FCMDevice.objects.filter(registration_id=fcm_device.get('registration_id'))
            if devices.exists():
                devices.update(user=user, active=True)
            else:
                try:
                    fcm_device_serializer = FCMDeviceSerializer(data=fcm_device, context={'request': request})
                    fcm_device_serializer.is_valid(raise_exception=True)
                    fcm_device_serializer.save(user=user)
                except Exception as err:
                    print('fcm error', err)
        user_serializer = AccountAuthUserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


"""class DoctorRegistrationAPIView(CreateAPIView):
    serializer_class = AccountRegistrationSerializerDoctor
    authentication_classes = []
    permission_classes = []"""


class AccountAuthProfileDetalAPIView(RetrieveUpdateAPIView):
    serializer_class = AccountAuthUserSerializer
    queryset = User.objects.none()

""" def get_serializer_class(self):
        if self.request.user.user_type == User.USER_TYPE_DOCTOR:
            return AccountAuthUserDoctorSerializer
        elif self.request.user.user_type == User.USER_TYPE_PATIENT:
            return AccountAuthUserPatientSerializer
        else:
            return AccountAuthUserSerializer """

def get_object(self):
        return self.request.user


class VerfiyEmailExistAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response({
                'success': False,
                'message': 'Email field required.'
            }, status=400)
        is_email = email_address_exists(email)
        if is_email:
            return Response({
                'success': True,
                'message': 'An account already exists with this email address.'
            })
        return Response({
            'success': False,
            'message': 'Email address not found.'
        }, status=404)


class AccountDeleteAPIView(DestroyAPIView):
    serializer_class = AccountAuthUserSerializer
    queryset = User.objects.none()

    def get_object(self):
        return self.request.user
