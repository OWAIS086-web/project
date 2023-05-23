from django.conf import settings
from djstripe import enums
from djstripe.models import PaymentIntent, PaymentMethod, Customer
from stripe.error import StripeError


def get_stripe_key():
    if settings.STRIPE_LIVE_MODE:
        return settings.STRIPE_LIVE_SECRET_KEY
    return settings.STRIPE_TEST_SECRET_KEY


def create_payment_method(card, billing_details={}):
    try:
        pm_method = PaymentMethod._api_create(type='card', card=card, billing_details=billing_details)
    except StripeError as err:
        print(err)
        return None
    return pm_method

    # if attach:
    #     fingerprint = pm_method.card.fingerprint
    #     fingerprint_exist = PaymentMethod.objects.filter(card__fingerprint=fingerprint,
    #                                                      customer=customer)
    #
    #     if fingerprint_exist.exists():
    #         pm_serializer = PaymentMethodSerializer(fingerprint_exist.first())
    #         return Response(pm_serializer.data)


def attach_payment_method(payment_method, customer):
    fingerprint = payment_method.card.fingerprint
    fingerprint_exist = PaymentMethod.objects.filter(card__fingerprint=fingerprint, customer=customer).exists()
    if fingerprint_exist:
        return fingerprint_exist.first()
    return customer.add_payment_method(payment_method=payment_method.id)


def create_payment_intent(payment_method, customer, data, save_method=False):
    payment_intent = PaymentIntent._api_create(
        currency='usd',
        customer=customer.id,
        payment_method=payment_method,
        **data
    )
    return payment_intent


def create_subscription_payment(plan, payment_method, customer, receipt_email=None, save_method=False):
    # try:
    #     payment_method_instance = PaymentMethod.objects.get(id=payment_method)
    # except:
    #     return None

    amount = int(plan.price * 100)
    metadata = {
        'plan_id': plan.id,
        'plan_title': plan.title,
        'plan_period_type': plan.plan_period_type,
        'plan_price': str(plan.price),
        'plan_price_currency': 'usd',
        'plan_grace_period': plan.grace_period,
    }
    payment_data = {
        'amount': amount,
        # 'amount_capturable': amount,
        # 'amount_received': amount,
        'payment_method_types': ['card'],
        'confirmation_method': enums.ConfirmationMethod.manual,
        'capture_method': enums.CaptureMethod.automatic,
        'confirm': True,
        # 'confirm': False,
        'metadata': metadata,
    }
    if save_method:
        # payment_data['confirm'] = True
        payment_data['setup_future_usage'] = 'off_session'
        # payment_data['off_session'] = True

    if receipt_email:
        payment_data['receipt_email'] = receipt_email

    print('initiate create intent')
    payment_intent = create_payment_intent(payment_method, customer, payment_data, save_method=save_method)
    payment_intent_id = payment_intent.id

    print('intent created', payment_intent_id)
    # payment_intent._api_confirm()
    instance, created = PaymentIntent._get_or_create_from_stripe_object(payment_intent)
    print('instance', instance)
    # payment_intent_instance = payment_intent.sync_from_stripe_data(payment_intent)
    # print(data)
    print('intent confirming', payment_intent_id)
    # instance = PaymentIntent.sync_from_stripe_data(payment_intent)
    # confirm_intent = instance._api_confirm()
    # print('intent confirmed', payment_intent_id)
    return instance


def create_subscription_upgrade_payment(price, plan, payment_method, customer, receipt_email=None):
    amount = int(price * 100)
    metadata = {
        'plan_id': plan.id,
        'plan_title': plan.title,
        'plan_period_type': plan.plan_period_type,
        'plan_price': str(plan.price),
        'plan_price_currency': 'usd',
        'plan_grace_period': plan.grace_period,
        'description': f'Upgrade plan to {plan.title} - {plan.get_plan_period_type_display}'
    }
    payment_data = {
        'amount': amount,
        'payment_method_types': ['card'],
        'confirmation_method': enums.ConfirmationMethod.manual,
        'capture_method': enums.CaptureMethod.automatic,
        'confirm': True,
        'metadata': metadata,
    }

    if receipt_email:
        payment_data['receipt_email'] = receipt_email

    payment_intent = create_payment_intent(payment_method, customer, payment_data)
    payment_intent_id = payment_intent.id

    print('intent created', payment_intent_id)
    instance, created = PaymentIntent._get_or_create_from_stripe_object(payment_intent)
    return instance
