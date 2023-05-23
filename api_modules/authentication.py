from rest_framework.authentication import TokenAuthentication
from django.utils.translation import gettext_lazy as _
import base64
import binascii

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import HTTP_HEADER_ENCODING, exceptions


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed({
                'detail': _('Invalid token.'),
                'success': False,
                'code': 'invaild',
            })

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)
