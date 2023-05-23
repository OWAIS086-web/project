from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from modules.model_mixins import TimeStampModel

DEVICE_IOS = 0
DEVICE_ANDROID = 1
DEVICE_AMAZON = 2
DEVICE_WINDOWS_PHONE = 3
DEVICE_CHROME_APPS = 4
DEVICE_CHROME_WEB_PUSH = 5
DEVICE_WINDOWS = 6
DEVICE_SAFARI = 7
DEVICE_FIREFOX = 8
DEVICE_MACOS = 9
DEVICE_ALEXA = 10
DEVICE_EMAIL = 11
DEVICE_HUAWEI_APP_BUILDS = 13
DEVICE_SMS = 14

DEVICE_CHOICES = (
    (DEVICE_IOS, 'iOS'),
    (DEVICE_ANDROID, 'Android'),
    (DEVICE_AMAZON, 'Amazon'),
    (DEVICE_WINDOWS_PHONE, 'WindowsPhone (MPNS)'),
    (DEVICE_CHROME_APPS, 'Chrome Apps / Extensions'),
    (DEVICE_CHROME_WEB_PUSH, 'Chrome Web Push'),
    (DEVICE_WINDOWS, 'Windows (WNS)'),
    (DEVICE_SAFARI, 'Safari'),
    (DEVICE_FIREFOX, 'Firefox'),
    (DEVICE_MACOS, 'MacOS'),
    (DEVICE_ALEXA, 'Alexa'),
    (DEVICE_EMAIL, 'Email'),
    (DEVICE_HUAWEI_APP_BUILDS, 'Huawei App Gallery Builds. Not for Huawei Devices using FCM'),
    (DEVICE_SMS, 'SMS'),
)


class OneSignalDevice(TimeStampModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='onesignal_devices')
    app_id = models.CharField(_('App ID'), max_length=250, editable=False, null=True)
    device_id = models.CharField(_('Device ID'), max_length=250, editable=False)

    device_type = models.PositiveIntegerField(choices=DEVICE_CHOICES)
    identifier = models.CharField(_('Identifier'), max_length=250, null=True, blank=True,
                                  help_text=_('For Push Notifications, this is the Push Token Identifier from '
                                              'Google or Apple. For Apple Push identifiers, you must strip all '
                                              'non alphanumeric characters.')
                                  )
    email_address = models.EmailField(_('Email Addresses'), null=True, blank=True,
                                      help_text=_('set the full email address email@email.com and make sure'
                                                  ' to set device_type to 11.')
                                      )

    phone_number = models.CharField(_('Phone Number'), max_length=20, null=True, blank=True,
                                    help_text=_('set the E.164 format and make sure to set device_type to 14.')
                                    )

    language = models.CharField(_('Language'), max_length=10, default='en',
                                help_text=_('Language code. Typically lower case two letters, except for Chinese '
                                            'where it must be one of zh-Hans or zh-Hant. Example: en')
                                )

    device_model = models.CharField(_('Device Model'), max_length=250,
                                    help_text=_('Device make and model.')
                                    )

    device_os = models.CharField(_('Device OS'), max_length=250,
                                 help_text=_('Device operating system version.')
                                 )

    latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    country = CountryField(_('Country'), null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('OneSignal Device')
        verbose_name_plural = _('OneSignal Devices')
