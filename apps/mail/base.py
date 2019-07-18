from django.contrib import messages
from django.template import engines
from django.utils.html import format_html
from django.urls import reverse

from . import tasks
from .models import Mail
from .libs.serialize import serialize


class MailBase:
    @classmethod
    def process(cls, user, data=None, request=None, **kwargs):
        return data

    @classmethod
    def render_body(cls, data):
        django_engine = engines['django']
        template = django_engine.get_template(cls.template)
        return template.render(data)

    @classmethod
    def render_subject(cls, data):
        django_engine = engines['django']
        template = django_engine.from_string(cls.subject)
        return template.render(data)

    def __new__(cls, user, data=None, request=None, **kwargs):
        data = serialize(cls.process(user, data, request, **kwargs))
        body = cls.render_body(data)
        subject = cls.render_subject(data)
        mail = Mail.objects.create(
            name=cls.name,
            user=user,
            data=data,
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
