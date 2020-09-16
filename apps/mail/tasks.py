import logging
import json
import requests

from django.conf import settings

from workers import task


log = logging.getLogger(__name__)


def _sendgrid_send(mail):
    """
    Uses SendGrid API to send email.
    Do not call this function directly.
    """
    headers = {
        'authorization': 'Bearer {0}'.format(settings.SENDGRID_API_KEY),
        'content-type': 'application/json'
    }

    to_email = getattr(mail.user, mail.user.get_email_field_name())
    try:
        to_name = mail.user.get_full_name()
    except:
        to_name = to_email

    payload = {
        'personalizations': [{
            'to': [{
                'email': to_email,
                'name': to_name,
            }]
        }],
        'from': {
            'email': settings.SENDGRID_FROM_EMAIL,
            'name': settings.SENDGRID_FROM_NAME
        },
        'subject': mail.subject,
        'content': [{
            'value': mail.body,
            'type': 'text/html'
        }]
    }

    response = requests.post(
        settings.SENDGRID_URL, data=json.dumps(payload), headers=headers
    )
    mail.api_response_code = response.status_code
    mail.api_response_text = response.text

    if (response.status_code < 200) or (response.status_code > 299):
        mail.status = Mail.ERROR
        mail.save()
        raise Exception(response.text)

    mail.status = Mail.SENT
    mail.save()

    return response


def _smtp_send(mail):
    """
    Uses SMTP settings to send an email.
    Do not call this function directly.
    """
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


@task()
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

    # If you want add more backends, handle them here.
    if settings.EMAIL_BACKEND == 'sendgrid':
        return _sendgrid_send(mail)
    else:
        return _smtp_send(mail)

