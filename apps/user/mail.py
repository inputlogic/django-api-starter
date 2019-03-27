from django.conf import settings

from ..mail.models import Mail


def mail_reset_password(user, reset_token, request=None):
    reset_url = settings.RESET_PASSWORD_URL.format(
        reset_token=reset_token,
        user_id=user.id
    )
    return Mail.send(
        settings.MAIL_KEY_PASSWORD,
        user,
        {
            'reset_url': reset_url
        },
        request
    )


def mail_welcome_user(user, request=None):
    return Mail.send(
        settings.MAIL_KEY_WELCOME,
        user,
        {
            'email': user.email,
        },
        request
    )
