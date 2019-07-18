import logging
import json
import requests

from django.conf import settings

from workers import task


log = logging.getLogger(__name__)


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

    headers = {
        'authorization': 'Bearer {0}'.format(settings.SENDGRID_API_KEY),
        'content-type': 'application/json'
    }

    payload = {
        'personalizations': [{
            'to': [{
                'email': mail.user.email,
                'name': mail.user.email,
                # ___CHANGEME___ if users have first and last names
#                'name': '{} {}'.format(
#                    mail.user.first_name,
#                    mail.user.last_name
#                ).strip()
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
