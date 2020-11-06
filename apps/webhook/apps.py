import logging

from django.apps import AppConfig


log = logging.getLogger(__name__)


class WebhookConfig(AppConfig):
    name = 'apps.webhook'

    def ready(self):
        from django.conf import settings

        if not settings.WEBHOOKS_NOTIFY_URL:
            log.warning("WEBHOOKS_NOTIFY_URL not set, but 'apps.webhook' is installed.")
        else:
            from . import signals
