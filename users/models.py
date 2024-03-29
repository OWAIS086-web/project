from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from subscriptions.models import Subscription


class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.

    USER_TYPE_DOCTOR = 'doctor'
    USER_TYPE_PATIENT = 'patient'

    USER_TYPE_CHOICES = (
        (USER_TYPE_DOCTOR, _('Doctor')),
        (USER_TYPE_PATIENT, _('Patient')),
    )

    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    email = models.EmailField(_('Email'), unique=True)

    user_type = models.CharField(_('User Type'), choices=USER_TYPE_CHOICES, max_length=10, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        if self.email:
            return f'{self.email}'
        return '%s' % self.username

    class Meta:
        verbose_name_plural = _('List of all Users')

    @property
    def get_subscription(self):
        try:
            return self.subscription
        except Subscription.DoesNotExist:
            return None

    @property
    def get_active_subscription(self):
        try:
            return self.subscription
        except Subscription.DoesNotExist:
            return None
        # return self.pk
