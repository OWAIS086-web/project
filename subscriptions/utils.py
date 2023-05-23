from django.utils.translation import ugettext_lazy as _
from subscriptions.models import Subscription, SubscriptionPlan


def price_for_days(price, grace_period, days):
    charge_amount = (price / int(grace_period)) * int(days)
    return charge_amount


def create_subscription_from_apple_inapp(receipt, is_api=True):
    user = receipt.user
    product_id = receipt.product_id
    try:
        subscription = user.subscription
        if subscription.is_active:
            return None
    except Subscription.DoesNotExist:
        subscription = Subscription(user=user, payment_type=Subscription.PAYMENT_TYPE_APPLE_IAP)
    plans = SubscriptionPlan.objects.filter(apple_product_id=product_id)
    plan = None

    if plans.exists():
        plan = plans.first()
    else:
        if is_api:
            from rest_framework.validators import ValidationError
            raise ValidationError(_('Product ID not matching with any plan.'))

        from django.core.exceptions import ValidationError
        raise ValidationError('Product ID not matching with any plan..')

    subscription.started_at = receipt.original_purchase_date
    subscription.ended_at = receipt.expires_date
    subscription.is_trial_period = receipt.is_trial_period
    if plan:
        subscription.plan = plan
        subscription.title = plan.title
        subscription.plan_period_type = plan.plan_period_type
    subscription.save()
    return subscription
