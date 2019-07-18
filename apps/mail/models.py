from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.html import format_html


class Mail(models.Model):
    PENDING = 'pending'
    SENT = 'sent'
    TEST = 'test mode'
    ERROR = 'error'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    data = JSONField()
    body = models.TextField(default='')
    subject = models.CharField(max_length=250, default='')
    name = models.CharField(max_length=250, verbose_name='type')
    status = models.CharField(max_length=10, default=PENDING)
    api_response_code = models.IntegerField(null=True)
    api_response_text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Mail: {0} - {1}>'.format(self.name, self.user.email)

    class Meta:
        verbose_name = 'mail'
        verbose_name_plural = 'outbox'

    @property
    def email(self):
        return self.user.email
