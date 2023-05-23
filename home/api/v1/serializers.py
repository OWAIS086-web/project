from rest_framework import serializers

from home.models import *


class EmailInvitationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class AppStoreLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppStoreLink
        fields = '__all__'
