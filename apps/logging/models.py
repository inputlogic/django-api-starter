from rest_framework_tracking.models import APIRequestLog as BaseAPIRequestLog


class APIRequestLog(BaseAPIRequestLog):
    class Meta:
        proxy = True
        verbose_name = 'API request log'
        verbose_name_plural = 'API request logs'
