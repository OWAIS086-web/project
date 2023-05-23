from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OnesignalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onesignal_app'
    verbose_name = _('OneSignal App')

    def ready(self):
        try:
            import onesignal_app.signals
        except ImportError:
            pass
