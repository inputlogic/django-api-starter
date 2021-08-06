from django.conf import settings

from apps.mail.models import Mail


def send_forgot_password_email(user, reset_token):
    reset_url = settings.RESET_PASSWORD_URL.format(
        reset_token=reset_token,
        user_id=user.id
    )
    Mail.send('ForgotPassword', user, reset_url=reset_url)


def send_welcome_email(user):
    Mail.send('WelcomeUser', user)
