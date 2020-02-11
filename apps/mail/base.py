from django.contrib import messages
from django.template import engines
from django.utils.html import format_html
from django.utils.text import get_valid_filename
from django.urls import reverse

from . import tasks
from .models import Mail
from .libs.serialize import serialize
from .libs.camel_space_to_spaces import camel_space_to_spaces


class MailBase:
    @classmethod
    def process_args(cls, user, request=None, *args, **kwargs):
        return {
            'user': user,
            'request': request,
            **kwargs
        }

    @classmethod
    def get_name(cls):
        try:
            return cls.name
        except AttributeError:
            name = cls.__name__
            if name.startswith('Mail'):
                name = name[4:]
            return name

    @classmethod
    def get_subject(cls):
        try:
            return cls.subject
        except AttributeError:
            name = cls.get_name()
            subject = camel_space_to_spaces(name).capitalize()
            return subject

    @classmethod
    def get_template(cls):
        try:
            return cls.template
        except AttributeError:
            name = cls.get_name()
            path = 'email/{name}.html'.format(
                name=get_valid_filename(camel_space_to_spaces(name))
            )
            return path

    @classmethod
    def render_body(cls, ctx):
        django_engine = engines['django']
        template = django_engine.get_template(cls.get_template())
        return template.render(ctx)

    @classmethod
    def render_subject(cls, ctx):
        django_engine = engines['django']
        template = django_engine.from_string(cls.get_subject())
        return template.render(ctx)

    @classmethod
    def send(cls, user, request=None, admin_feedback=False, *args, **kwargs):
        ctx = serialize(cls.process_args(user, request, *args, **kwargs))
        body = cls.render_body(ctx)
        subject = cls.render_subject(ctx)
        mail = Mail.objects.create(
            name=cls.get_name(),
            user=user,
            data=ctx,
            body=body,
            subject=subject
        )
        tasks.send_email(mail.id)  # Sets a background task to send the email

        if admin_feedback and request is not None:
            mail_url = reverse(
                'admin:%s_%s_change' % ('mail', 'mail'),
                args=[mail.id],
            )
            msg = format_html(
                'The mail message "<a href ="{}">{}</a>" was generated and is awaiting delivery.',
                mail_url,
                mail,
            )
            messages.success(request, msg)

        return mail
