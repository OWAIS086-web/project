from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from djstripe.models import *


class StripeCardSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=True)
    exp_month = serializers.IntegerField(required=True)
    exp_year = serializers.IntegerField(required=True)
    cvc = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        from djstripe.models import PaymentMethod, Customer
        return validated_data


class StripeCardSerializerPaymentMethod(serializers.Serializer):
    number = serializers.IntegerField(required=True)
    exp_month = serializers.IntegerField(required=True)
    exp_year = serializers.IntegerField(required=True)
    cvc = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        return validated_data


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class BalanceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceTransaction
        fields = '__all__'
