import logging
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template import engines
from django.utils.html import format_html
from django.urls import reverse

from . import tasks


log = logging.getLogger(__name__)


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

    @staticmethod
    def render_body(name, data):
        template_path = settings.MAIL_REGISTRY[name]['template']
        django_engine = engines['django']
        template = django_engine.get_template(template_path)
        return template.render(data)

    @staticmethod
    def render_subject(name, data):
        subject = settings.MAIL_REGISTRY[name]['subject']
        django_engine = engines['django']
        template = django_engine.from_string(subject)
        return template.render(data)

    @staticmethod
    def send(name, user, data, request=None):
        body = Mail.render_body(name, Mail.serialize(data))
        subject = Mail.render_subject(name, Mail.serialize(data))
        mail = Mail.objects.create(
            name=name,
            user=user,
            data=Mail.serialize(data),
            body=body,
            subject=subject
        )
        tasks.send_email(mail.id) # Sets a background task to send the email

        if (request != None):
            mail_url = reverse(
                'admin:%s_%s_change' % ('mail', 'mail'),
                args=[mail.id],
            )
            msg = format_html(
                'The mail message "<a href ="{}">{}</a>" was generated successfully.',
                mail_url,
                mail,
            )
            messages.success(request, msg)

        return mail

    @staticmethod
    def serialize(data):
        if type(data) is dict:
            return {k: Mail.serialize(v) for (k, v) in data.items()}
        elif type(data) is datetime:
            return data.isoformat()
        return data

    @property
    def email(self):
        return self.user.email
