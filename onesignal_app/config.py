import requests
from django.conf import settings


class OneSignal(object):
    api_url = "https://onesignal.com/api/v1"

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Basic {settings.ONE_SIGNAL_API_KEY}",
            "content-type": "application/json"
        }

    def post(self, url_path, payload):
        payload['app_id'] = settings.ONE_SIGNAL_APP_ID,
        api_url = f'{self.api_url}/{url_path}/'
        res = requests.post(
            api_url,
            json=payload,
            headers=self.headers,
        )
        return res

    def send_notification(self, notification=None):
        if notification:
            payload = {
                'contents': {
                    "en": notification.title,
                },
                'include_player_ids': ['b39e7fab-ceda-4be2-91e4-6beb8cf80902']
            }
            return self.post(payload)
        return None
