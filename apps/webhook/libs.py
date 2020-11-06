import requests
from django.conf import settings


def notify(title='Triggered by Djano signal', branch='master'):
    response = requests.post(
        settings.WEBHOOKS_NOTIFY_URL,
        params={'trigger_title': title, 'trigger_branch': branch},
    )
    if (response.status_code < 200) or (response.status_code > 299):
        raise Exception(response.text)
    return response
