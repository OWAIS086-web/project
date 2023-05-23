from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from datetime import timedelta

from modules.model_mixins import TimeStampModel


class SubscriptionPlan(TimeStampModel):
    PERIOD_CUSTOM = 'custom'
    PERIOD_MONTHLY = 'monthly'
    PERIOD_YEARLY = 'yearly'

    PERIOD_TYPE_CHOICES = (
        (PERIOD_MONTHLY, _('Monthly')),
        (PERIOD_YEARLY, _('Yearly')),
        (PERIOD_CUSTOM, _('Custom')),
    )

    title = models.CharField(_('Title'), max_length=120)
    slug = AutoSlugField(populate_from=['title'], unique=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=10)
    plan_period_type = models.CharField(_('Plan Period Type'), choices=PERIOD_TYPE_CHOICES, max_length=10)
    apple_product_id = models.CharField(_('Apple Product ID'), max_length=32, null=True)
    description = models.TextField(
        blank=True,
        help_text=_('A description of the subscription plan')
    )

    grace_period = models.PositiveIntegerField(
        _('Grace Period'),
        default=0,
        help_text=_(
            'How many days after the subscription ends before the subscription expires.'
        ),
    )
    upgrade_from_plans = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('Subscription Plan')
        verbose_name_plural = _('Subscription Plans')
        constraints = [
            models.UniqueConstraint(
                fields=['apple_product_id'],
                name='plan_apple_product_id_unique',
                condition=models.Q(apple_product_id__isnull=False)
            )
        ]

    def clean(self):
        # plan_period_type = data.get('plan_period_type')
        # grace_period = data.get('grace_period')
        # if self.plan_period_type == self.PERIOD_MONTHLY
        if self.pk:
            check_product_id = SubscriptionPlan.objects.filter(apple_product_id=self.apple_product_id).exclude(
                id=self.pk)
            if check_product_id.exists():
                raise ValidationError(_('Apple Product ID already used in another plan.'))
        else:
            check_product_id = SubscriptionPlan.objects.filter(apple_product_id=self.apple_product_id)
            if check_product_id.exists():
                raise ValidationError(_('Apple Product ID already used in another plan.'))

        # print(data)

    def save(self, *args, **kwargs):
        if self.plan_period_type == self.PERIOD_MONTHLY and (self.grace_period == 0 or self.grace_period == ''):
            self.grace_period = 30
        elif self.plan_period_type == self.PERIOD_YEARLY and (self.grace_period == 0 or self.grace_period == ''):
            self.grace_period = 365
        super(SubscriptionPlan, self).save(*args, **kwargs)


class Subscription(TimeStampModel):
    PERIOD_CUSTOM = 'custom'
    PERIOD_MONTHLY = 'monthly'
    PERIOD_YEARLY = 'yearly'

    PERIOD_TYPE_CHOICES = (
        (PERIOD_MONTHLY, _('Monthly')),
        (PERIOD_YEARLY, _('Yearly')),
        (PERIOD_CUSTOM, _('Custom')),
    )

    PAYMENT_TYPE_APPLE_IAP = 'apple_iap'
    PAYMENT_TYPE_STRIPE_CARD = 'stripe_card'

    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_APPLE_IAP, _('apple_iap')),
        (PAYMENT_TYPE_STRIPE_CARD, _('Stripe Card')),
    )

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey('subscriptions.SubscriptionPlan', on_delete=models.SET_NULL, null=True,
                             related_name='subscriptions')
    title = models.CharField(_('Title'), max_length=250, null=True, blank=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=10)
    plan_period_type = models.CharField(_('Plan Period Type'), choices=PERIOD_TYPE_CHOICES, max_length=10)

    is_cancelled = models.BooleanField(
        _('Cancelled'),
        default=False,
        help_text=_('whether this subscription is cancelled or not'),
    )

    payment_type = models.CharField(_('Payment Type'), choices=PAYMENT_TYPE_CHOICES, max_length=20,
                                    default=None, null=True, blank=True)

    is_trial_period = models.BooleanField(_('Trial Period'), default=False)
    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)
    ended_at = models.DateTimeField(_('Ended at'), null=True, blank=True)
    cancelled_at = models.DateTimeField(_('Cancelled at'), null=True, blank=True)
    description = models.TextField(_('Description'), blank=True)
    upgrade_charge_amount = models.DecimalField(_('Upgrade Charge Amount'), decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'{self.user.username} | {self.title}'

    @property
    def get_status(self):
        now = timezone.now()
        if not self.is_cancelled and (self.ended_at and self.ended_at < now):
            return True
        return False

    @property
    def is_expired(self):
        now = timezone.now()
        if self.ended_at and now >= self.ended_at:
            return True
        return False

    @property
    def is_active(self):
        now = timezone.now()
        if self.ended_at and now < self.ended_at:
            return True
        return False

    @property
    def get_expired_in_days(self):
        now = timezone.now()
        if self.ended_at and now < self.ended_at:
            days = (self.ended_at - now).days
            return int(days)

        return 0

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def save(self, *args, **kwargs):
        if not self.pk and self.plan:
            plan = self.plan
            if not self.plan_period_type:
                self.plan_period_type = plan.plan_period_type

            if not self.price or self.price == 0:
                self.price = plan.price

            self.started_at = timezone.now()

            if plan.plan_period_type == self.PERIOD_MONTHLY and not self.ended_at:
                self.ended_at = self.started_at + timedelta(days=30)
            if plan.plan_period_type == self.PERIOD_YEARLY and not self.ended_at:
                self.ended_at = self.started_at + timedelta(days=365)
        if self.cancelled_at:
            self.ended_at = self.cancelled_at
        super(Subscription, self).save(*args, **kwargs)
