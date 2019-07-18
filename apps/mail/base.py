from django.contrib import messages
from django.template import engines
from django.utils.html import format_html
from django.urls import reverse

from . import tasks
from .models import Mail
from .libs.serialize import serialize


class MailBase:
    @classmethod
    def process_context(cls, user, request=None, **kwargs):
        return {
            'user': user,
            'request': request,
            **kwargs
        }

    @classmethod
    def render_body(cls, ctx):
        django_engine = engines['django']
        template = django_engine.get_template(cls.template)
        return template.render(ctx)

    @classmethod
    def render_subject(cls, ctx):
        django_engine = engines['django']
        template = django_engine.from_string(cls.subject)
        return template.render(ctx)

    def __new__(cls, user, request=None, **kwargs):
        ctx = serialize(cls.process_context(user, request, **kwargs))
        body = cls.render_body(ctx)
        subject = cls.render_subject(ctx)
        mail = Mail.objects.create(
            name=cls.name,
            user=user,
            data=ctx,
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
