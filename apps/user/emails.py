import logging

from django.conf import settings
from rest_framework.exceptions import ParseError

from libs.email import send_template


def new_account(email):
    return send_template(
        settings.SENDGRID_TEMPLATE_NEW_ACCOUNT,
        email,
        name='New Account'
    )


def forgot_password(reset_token, user):
    return send_template(
        settings.SENDGRID_TEMPLATE_FORGOT_PASSWORD,
        user.email,
        custom_tags={
            '[RESET_URL]': settings.RESET_PASSWORD_URL.format(
                reset_token=reset_token, user_id=user.id),
            '[USER_EMAIL]': user.email
            },
        name='Forgot Password'
    )
