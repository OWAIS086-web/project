from django.utils.translation import ugettext_lazy as _
from rest_framework.views import *
from rest_framework.generics import *
from stripe.error import StripeError

from .serializers import *


class PaymentMethodAPIView(ListCreateAPIView):
    serializer_class = StripeCardSerializerPaymentMethod
    queryset = PaymentMethod.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PaymentMethodSerializer
        return super(self.__class__, self).get_serializer_class()

    def get_customer(self):
        from djstripe.models import Customer
        customer, created = Customer.get_or_create(self.request.user)
        return customer

    def get_queryset(self):
        return PaymentMethod.objects.filter(customer=self.get_customer())

    def create(self, request, *args, **kwargs):
        customer = self.get_customer()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            name = data.pop('name', None)
            if name is None:
                name = request.user.get_full_name().strip()
            from djstripe.models import Card, Customer, PaymentMethod
            billing_details = {
                'name': name,
                'email': request.user.email
            }
            try:
                method = PaymentMethod._api_create(type='card', card=data, billing_details=billing_details)
            except StripeError as err:
                print(err)
                return Response({'detail': _(err.user_message)}, status=400)
            fingerprint = method.card.fingerprint
            fingerprint_exist = PaymentMethod.objects.filter(card__fingerprint=fingerprint,
                                                             customer=customer)
            if fingerprint_exist.exists():
                pm_serializer = PaymentMethodSerializer(fingerprint_exist.first())
                return Response(pm_serializer.data)
            try:
                customer_method = customer.add_payment_method(payment_method=method.id)
            except StripeError as err:
                return Response({'detail': _(err.user_message)}, status=400)
            pm_serializer = PaymentMethodSerializer(customer_method)
            return Response(pm_serializer.data)

        return Response({'detail': _('Failed add payment method')}, status=400)


class PaymentMethodDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = StripeCardSerializer
    queryset = PaymentMethod.objects.none()

    def get_customer(self):
        from djstripe.models import Customer
        customer, created = Customer.get_or_create(self.request.user)
        return customer

    def get_queryset(self):
        return PaymentMethod.objects.filter(customer=self.get_customer())
