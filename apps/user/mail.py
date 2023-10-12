from django.conf import settings

from libs.encode import dict_to_base64
from apps.mail.models import Mail


def send_forgot_password_email(user, reset_token):
    reset_url = settings.RESET_PASSWORD_URL.format(
        state=dict_to_base64({
            'token': reset_token,
            'userId': user.id,
        })
    )
    Mail.send('ForgotPassword', user, reset_url=reset_url)


def send_welcome_email(user):
    Mail.send('WelcomeUser', user)
