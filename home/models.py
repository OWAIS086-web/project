from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from modules.model_mixins import TimeStampModel


class PrivacyPolicy(models.Model):
    title = models.CharField(_('Title'), max_length=160)
    # slug = AutoSlugField(populate_from=['tit'])
    description = models.TextField(_('Description'), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policy')


class TermsAndCondition(models.Model):
    title = models.CharField(_('Title'), max_length=160)
    # slug = AutoSlugField(populate_from=['tit'])
    description = models.TextField(_('Description'), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Terms & Conditions')
        verbose_name_plural = _('Terms & Conditions')


class AppStoreLink(TimeStampModel):
    apple_store_link = models.URLField(_('Apple Store Link'), null=True, blank=True)
    google_play_store_link = models.URLField(_('Google Play Store Link'), null=True, blank=True)
    apple_store_logo = models.ImageField(_('Apple Store Logo'), upload_to='home/app_stores', null=True, blank=True)
    google_play_store_logo = models.ImageField(_('Google Play Store Logo'), upload_to='home/app_stores', null=True,
                                               blank=True)

    def __str__(self):
        return 'App Stores Link'

    class Meta:
        verbose_name = _('App Stores Link')
        verbose_name_plural = _('App Stores Link')
