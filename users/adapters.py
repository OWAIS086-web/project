from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.http import HttpRequest
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = f'{self.get_from_email()}'
        if settings.DEFAULT_EMAIL_SENDER_NAME:
            from_email = f'{settings.DEFAULT_EMAIL_SENDER_NAME} <{self.get_from_email()}>'
        from home.models import AppStoreLink
        try:
            app_store_links = AppStoreLink.objects.first()

        except AppStoreLink.DoesNotExist:
            app_store_links = None

        if app_store_links:
            app_link_android = app_store_links.google_play_store_link
            app_link_ios = app_store_links.apple_store_link
            context['app_link_android'] = app_link_android
            context['app_link_ios'] = app_link_ios

        gs_bucket_name = settings.GS_BUCKET_NAME
        context['gs_bucket_name'] = gs_bucket_name
        context['app_store_links'] = app_store_links

        # print(context)

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        # if "txt" in bodies:
        #     msg = EmailMultiAlternatives(
        #         subject, bodies["txt"], from_email, to, headers=headers
        #     )
        #     if "html" in bodies:
        #         msg.attach_alternative(bodies["html"], "text/html")
        # else:
        #     msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
        #     msg.content_subtype = "html"  # Main content is now text/html

        if 'html' in bodies:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"
            return msg
        elif 'html' not in bodies and 'txt' in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            return msg
        return None


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "SOCIALACCOUNT_ALLOW_REGISTRATION", True)
