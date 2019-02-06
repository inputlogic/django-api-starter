import logging
import json

from django.conf import settings
import requests


log = logging.getLogger(__name__)


def send_template(template_id, to_email, to_name='', custom_tags={}, name=''):
    try:
        return send_template_base(
                template_id,
                to_email,
                to_name=to_name,
                custom_tags=custom_tags
                )
    except Exception as e:
        message = 'Error sending {0} email: {1}'.format(name or template_id, e)
        log.error(message)
        raise ParseError(detail=message)


def send_template_base(template_id, to_email, to_name='', custom_tags={}, name=''):
    """
    Sends an email via SendGrid API using a pre-determined SendGrid Template ID. Kwargs are used
    to pass in dynamic variables used in the template.
    """
    if not settings.SEND_EVENTS:
        print('simulate send email template: {0} to {1} with tags {2}'.format(name or template_id, to_email, custom_tags))
        return custom_tags

    headers = {
        'authorization': 'Bearer {0}'.format(settings.SENDGRID_API_KEY),
        'content-type': 'application/json'
    }

    payload = {
        'personalizations': [{
            'to': [{
                'email': to_email,
                'name': to_name
                }],
            'dynamic_template_data': custom_tags #for new version templates
            #'substitutions': custom_tags #for legacy templates
        }],
        'template_id': template_id,
        'from': {
            'email': settings.SENDGRID_FROM_EMAIL,
            'name': settings.SENDGRID_FROM_NAME
        }
    }

    response = requests.post(settings.SENDGRID_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 400:
        raise Exception(response.content)
    return response
