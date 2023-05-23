from .config import OneSignal


def onesignal_add_device(payload):
    url_path = 'players'
    client = OneSignal()
    return client.post(url_path=url_path, payload=payload)


def onesignal_send_notification(payload, include_player_ids=None):
    if include_player_ids is None:
        include_player_ids = []
    client = OneSignal()
    if include_player_ids and len(include_player_ids) > 0:
        payload['include_player_ids'] = include_player_ids

    return client.post(url_path='notifications', payload=payload)
