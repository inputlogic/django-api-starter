from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from .tasks import send_mail


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
                '''
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

    @staticmethod
    def send(template_name, user, **kwargs):
        template = Template.objects.get(name=template_name)
        layout = template.layout.body if template.layout else '{body}'

        subject = template.render_subject(kwargs)
        body = Layout.render(layout, template.render_body(kwargs))

        mail = Mail.objects.create(
            name=self.name,
            template=template,
            user=user,
            data=kwargs,
            subject=subject,
            body=body,
        )

        send_email(mail.id) # Background task

        return mail
