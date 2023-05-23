from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import permissions
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from ...utils import send_app_invitation_email


class SendEmailInvitationAPIView(CreateAPIView):
    serializer_class = EmailInvitationSerializer

    def create(self, request, *args, **kwargs):
        serializer = EmailInvitationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            current_site = get_current_site(request)
            email = validated_data.get('email')

            try:
                send_app_invitation_email(email, current_site, request)
                return Response({'message': 'Email sent.'}, status=200)
            except Exception as err:
                print(err)
                return Response({'message': 'Failed to sent email.'}, status=400)
        return Response(serializer.errors)


class DBUrlTest(APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        return Response({'db': settings.DATABASE_URL})


class AppStoreLinkAPIView(RetrieveAPIView):
    serializer_class = AppStoreLinkSerializer
    queryset = AppStoreLink.objects.all()

    def get_object(self):
        try:
            return AppStoreLink.objects.first()
        except AppStoreLink.DoesNotExist:
            raise Http404
