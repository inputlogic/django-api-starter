import logging
from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail as dj_send_mail


log = logging.getLogger(__name__)


def _smtp_send(mail):
    """
    Uses SMTP settings to send an email.
    Do not call this function directly.
    """
    from apps.mail.models import Mail

    to_email = getattr(mail.user, mail.user.get_email_field_name())

    try:
        sent = dj_send_mail(
            mail.subject,
            mail.body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=mail.body,
            fail_silently=False,
        )
        mail.status = Mail.SENT
        mail.save()
    except SMTPException as e:
        mail.status = Mail.ERROR
        mail.save()
        raise e

    return sent


@shared_task
def send_email(mail_id):
    """
    Do not call this task directly. Instead use a subclass of MailBase.

    """
    from apps.mail.models import Mail

    mail = Mail.objects.get(pk=mail_id)

    if not settings.SEND_MAIL:
        log.info('SEND_MAIL is not True! {}'.format(mail))
        mail.status = Mail.TEST
        mail.save()
        return

    return _smtp_send(mail)
