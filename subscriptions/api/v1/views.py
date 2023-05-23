from rest_framework.generics import *
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response

from .serializers import *


class SubscriptionPlanListAPIView(ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    pagination_class = None


class AvailableUpgradePlanListAPIView(ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    pagination_class = None

    def get_active_subscription(self):
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            return None

    def get_queryset(self):
        plan_id = self.kwargs.get('pk')
        # queryset = SubscriptionPlan.objects.filter(upgrade_from_plans__in=[plan_id])
        queryset = SubscriptionPlan.objects.filter(upgrade_from_plans__id__in=[plan_id]).exclude(id=plan_id)
        return queryset

    def list(self, request, *args, **kwargs):
        return super(self.__class__, self).list(request, *args, **kwargs)


class AccountActiveSubScriptionDetailAPIView(RetrieveAPIView):
    serializer_class = SubscriptionDetailSerializer
    queryset = Subscription.objects.none()

    def get_queryset(self):
        now = timezone.now()
        return Subscription.objects.filter(user=self.request.user, ended_at__gte=now)

    def get_object(self):
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            raise Http404


class AccountCancelSubScriptionAPIView(CreateAPIView):
    serializer_class = SubscriptionDetailSerializer
    queryset = Subscription.objects.none()

    def get_queryset(self):
        now = timezone.now()
        return Subscription.objects.filter(user=self.request.user, ended_at__gte=now)

    def get_object(self):
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        subscription = self.get_object()

        if not subscription.is_active:
            return Response({'detail': 'You don not have any active subscription'}, status=400)

        try:
            subscription.is_cancelled = True
            subscription.cancelled_at = timezone.now()
            subscription.save()

            serializer = SubscriptionDetailSerializer(subscription)
            return Response(serializer.data)
        except Exception as err:
            return Response({'detail': 'Failed to cancel subscription'}, status=400)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionCreateSerializer
    queryset = Subscription.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpgradeSubscriptionAPIView(CreateAPIView):
    serializer_class = UpgradeSubscriptionSerializer
    queryset = Subscription.objects.none()

    def get_active_subscription(self):
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            return None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, subscription=self.get_active_subscription())

    def create(self, request, *args, **kwargs):
        subscription = self.get_active_subscription()
        if not subscription:
            return Response({
                'detail': 'You do not have any active subscriptiopn.'
            }, status=400)
        return super(self.__class__, self).create(request, *args, **kwargs)


"""class CalculateUpgradePlanPriceAPIView(CreateAPIView):
    serializer_class = CalculateUpgradePlanPriceSerializer

    def get_active_subscription(self):
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            return None"""
def perform_create(self, serializer):
        serializer.save(user=self.request.user, subscription=self.get_active_subscription())

def post(self, request, *args, **kwargs):
        subscriptions = self.get_active_subscription()
        if subscriptions is None:
            return Response({'detail': 'You do not have any active subscription.'})
        return super(self.__class__, self).post(request, *args, **kwargs)
    




