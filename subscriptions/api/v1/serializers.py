from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from stripe.error import StripeError

from stripe_app.api.v1.serializers import StripeCardSerializer
from subscriptions.models import *


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    expire_in_days = serializers.IntegerField(source='get_expired_in_days', read_only=True, default=0)

    class Meta:
        model = Subscription
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(max_length=250, required=False, write_only=True)
    card = StripeCardSerializer(required=False, write_only=True)
    is_save_for_later = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'price': {
                'read_only': True
            },
            'plan_period_type': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            },
            'is_cancelled': {
                'read_only': True
            },
            'started_at': {
                'read_only': True
            },
            'ended_at': {
                'read_only': True
            },
            'cancelled_at': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        request = self.context['request']
        now = timezone.now()
        request = self.context['request']
        user = request.user
        try:
            subscription = user.subscription
        except Subscription.DoesNotExist:
            subscription = None

        if subscription and subscription.is_active:
            # subscriptions = user.subscriptions.filter(is_active=True)
            # if subscriptions.exists():
            raise serializers.ValidationError(_('You already have a active subscription'))

        if 'payment_method' not in attrs and 'card' not in attrs:
            raise serializers.ValidationError(_('Payment method or Card Details required.'))

        if 'payment_method' in attrs and 'card' in attrs:
            raise serializers.ValidationError(_('Payment method or Card, one is required.'))

        if 'payment_method' in attrs and attrs.get('payment_method') == "":
            raise serializers.ValidationError(_('Payment method is blank.'))

        if 'card' in attrs and attrs.get('card') is None:
            raise serializers.ValidationError(_('Card details should not be blank.'))

        # card = attrs.get('card', None)
        # is_save_for_later = attrs.get('is_save_for_later')
        # if is_save_for_later and card is None:
        #     raise serializers.ValidationError(_('Card is required to save.'))
        attrs['subscription'] = subscription

        return attrs

    def create(self, validated_data):
        payment_method = validated_data.get('payment_method', None)
        subscription = validated_data.pop('subscription', None)
        card = validated_data.get('card', None)
        user = validated_data.get('user')
        plan = validated_data.get('plan')
        is_save_for_later = validated_data.pop('is_save_for_later', False)
        created_method = None
        from djstripe.models import Customer
        customer, created = Customer.get_or_create(user)
        from stripe_app.utils import create_subscription_payment, create_payment_method, attach_payment_method

        if card and not payment_method:
            name = card.pop('name', None)
            if name is None:
                name = user.get_full_name().strip()
            billing_details = {
                'name': name,
                'email': user.email
            }
            created_method = create_payment_method(card=card, billing_details=billing_details)
            if created_method is None:
                raise serializers.ValidationError(_('Invalid Card Information.'))
            payment_method = created_method.id

        print('payment_method', payment_method)
        print('creating payment')

        try:
            payment = create_subscription_payment(plan=plan, payment_method=payment_method, customer=customer,
                                                  receipt_email=user.email, save_method=is_save_for_later)
            print(payment)
            print('payment successfull')
        except Exception as err:
            print(err)
            print('payment failed')

            raise serializers.ValidationError(_('Payment Failed.'))
        if payment:
            if subscription:
                now = timezone.now()
                ended_at = now + timedelta(days=plan.grace_period)
                subscription.started_at = now
                subscription.ended_at = ended_at
                subscription.title = plan.title
                subscription.price = plan.price
                subscription.upgrade_charge_amount = 0
                subscription.plan_period_type = plan.plan_period_type
                subscription.payment_type = Subscription.PAYMENT_TYPE_STRIPE_CARD
                subscription.is_cancelled = False
                subscription.is_trial_period = False
                subscription.description = plan.description
                subscription.save()
                if is_save_for_later and created_method:
                    from djstripe.models import PaymentMethod
                    sync_cards = PaymentMethod.attach(customer=customer, payment_method=created_method.id)
                    print(sync_cards)
                return subscription

            else:
                subscription = Subscription.objects.create(
                    user=user, plan=plan, payment_type=Subscription.PAYMENT_TYPE_STRIPE_CARD
                )
                if is_save_for_later and created_method:
                    from djstripe.models import PaymentMethod
                    sync_cards = PaymentMethod.attach(customer=customer, payment_method=created_method.id)
                    print(sync_cards)

                    #     print(sync_cards)
                    #     try:
                    #         attach_payment_method(created_method, customer)
                    #     except StripeError as err:
                    #         print(err)
                return subscription

        raise serializers.ValidationError(_('Payment Failed.'))


class UpgradeSubscriptionSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('user', 'price', 'plan_period_type', 'started_at', 'ended_at',
                            'cancelled_at', 'title', 'is_cancelled', 'is_trial_period',
                            'created_at', 'updated_at')

    def create(self, validated_data):
        payment_method = validated_data.pop('payment_method')
        plan = validated_data.get('plan')
        user = validated_data.get('user')
        subscription = validated_data.pop('subscription')

        if subscription.plan and subscription.plan == plan:
            raise serializers.ValidationError({
                'plan': _('You can not upgrade to same plan.')
            })
        if subscription.plan and subscription.plan_id not in plan.upgrade_from_plans.values_list('id', flat=True):
            raise serializers.ValidationError({
                'plan': _('You can not upgrade/downgrade to this plan.')
            })

        expired_in_days = subscription.get_expired_in_days
        grace_period = plan.grace_period
        from subscriptions.utils import price_for_days

        active_plan_charge_amount_left_days = round(price_for_days(
            subscription.plan.price, subscription.plan.grace_period, expired_in_days
        ), 2)

        new_plan_charge_amount_left_days = round(price_for_days(
            plan.price, plan.grace_period, expired_in_days
        ), 2)

        actual_charge_for_left_days = new_plan_charge_amount_left_days - active_plan_charge_amount_left_days

        subscription_days = (subscription.ended_at - subscription.started_at).days
        add_days = int(plan.grace_period) - int(subscription_days)

        charge_amount_for_add_days = round(price_for_days(plan.price, plan.grace_period, add_days), 2)

        actual_charge_amount = actual_charge_for_left_days + charge_amount_for_add_days

        from stripe_app.utils import create_subscription_upgrade_payment
        from djstripe.models import Customer

        customer, created = Customer.get_or_create(user)
        payment_intent_id = True

        try:
            payment_intent = create_subscription_upgrade_payment(
                price=actual_charge_amount, plan=plan, payment_method=payment_method,
                customer=customer, receipt_email=user.email
            )
        except StripeError as err:
            print(err)
            raise serializers.ValidationError(_('Payment Failed.'))

        if payment_intent:
            subscription.plan = plan
            subscription.title = plan.title
            subscription.price = plan.price
            subscription.plan_period_type = plan.plan_period_type
            subscription.upgrade_charge_amount = actual_charge_amount
            if int(plan.grace_period) > int(subscription_days):
                new_ended_date = subscription.ended_at + timedelta(days=add_days)
                print(new_ended_date)
                subscription.ended_at = new_ended_date
                subscription.save()
                return subscription

        raise serializers.ValidationError(_('Failed to upgrade plan.'))


class CalculateUpgradePlanPriceSerializer(serializers.Serializer):
    plan = serializers.IntegerField(write_only=True)
    plan_id = serializers.IntegerField(read_only=True)
    upgrade_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    def validate(self, attrs):
        plan_id = attrs.get('plan')
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError({'plan': 'Invalid Plan'})
        attrs['plan'] = plan
        return attrs

    def create(self, validated_data):
        plan = validated_data.get('plan')
        user = validated_data.get('user')
        subscription = validated_data.pop('subscription')
        if subscription.plan and subscription.plan == plan:
            raise serializers.ValidationError({
                'plan': _('You can not upgrade to same plan.')
            })
        if subscription.plan and subscription.plan_id not in plan.upgrade_from_plans.values_list('id', flat=True):
            raise serializers.ValidationError({
                'plan': _('You can not upgrade/downgrade to this plan.')
            })
        expired_in_days = subscription.get_expired_in_days
        print('expired_in_days', expired_in_days)
        grace_period = plan.grace_period
        print('grace_period', grace_period)
        from subscriptions.utils import price_for_days
        active_plan_charge_amount_left_days = round(price_for_days(
            subscription.plan.price, subscription.plan.grace_period, expired_in_days
        ), 2)
        print('active_plan_charge_amount_left_days: ', active_plan_charge_amount_left_days)
        new_plan_charge_amount_left_days = round(price_for_days(
            plan.price, plan.grace_period, expired_in_days
        ), 2)
        print('new_plan_charge_amount_left_days: ', new_plan_charge_amount_left_days)

        actual_charge_for_left_days = new_plan_charge_amount_left_days - active_plan_charge_amount_left_days
        print('actual_charge_for_left_days: ', actual_charge_for_left_days)
        subscription_days = (subscription.ended_at - subscription.started_at).days
        add_days = int(plan.grace_period) - int(subscription_days)
        print('add_days: ', add_days)
        charge_amount_for_add_days = round(price_for_days(plan.price, plan.grace_period, add_days), 2)
        print('charge_amount_for_add_days: ', charge_amount_for_add_days)

        actual_charge_amount = actual_charge_for_left_days + charge_amount_for_add_days

        return {
            'plan_id': plan.id,
            'upgrade_price': actual_charge_amount
        }
