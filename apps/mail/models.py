from django.conf import settings
from django.db import models
from django.template import engines
from django.core.exceptions import ValidationError

from .tasks import send_email


class Layout(models.Model):
    name = models.CharField(max_length=250, unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def render(layout_string, body_string):
        pieces = layout_string.split('{body}')
        return ''.join([pieces[0], body_string, pieces[1]])

    def save(self, *args, **kwargs):
        if '{body}' not in self.body:
            raise ValidationError({
                'body': '''
                    Must include {body} string somewhere in layout body. This is where
                    the template will get rendered.
                '''.strip()
            })
        return super().save(*args, **kwargs)


class Template(models.Model):
    name = models.CharField(max_length=250, unique=True)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    layout = models.ForeignKey(
        'mail.Layout',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def last_email_sent(self):
        return (
            Mail.objects.order_by('-created_at')
            .filter(name=self.name)
            .first()
        )

    def __str__(self):
        return '<Template: {0}>'.format(self.name)

    @staticmethod
    def _render(input, data):
        django_engine = engines['django']
        template = django_engine.from_string(input)
        return template.render(data)

    def render_body(self, data):
        return Template._render(self.body, data)

    def render_subject(self, data):
        return Template._render(self.subject, data)


class Mail(models.Model):
    PENDING = 'pending'
    SENT = 'sent'
    TEST = 'test mode'
    ERROR = 'error'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    template = models.ForeignKey(
        'mail.Template',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    data = models.JSONField()
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
        verbose_name_plural = ' Outbox'  # leading space, orders it first in admin

    @property
    def email(self):
        return self.user.email

    @staticmethod
    def send(name, user, **kwargs):
        if not kwargs.get('app_name'):
            kwargs['app_name'] = settings.APP_NAME

        if not kwargs.get('email'):
            kwargs['email'] = user.email

        template = Template.objects.get(name__iexact=name)
        layout = template.layout.body if template.layout else '{body}'

        subject = template.render_subject(kwargs)
        body = Layout.render(layout, template.render_body(kwargs))

        mail = Mail.objects.create(
            name=template.name,
            template=template,
            user=user,
            data=kwargs,
            subject=subject,
            body=body,
        )

        send_email(mail.id)  # Background task

        return mail
