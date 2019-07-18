from django.conf import settings

from ..mail.base import MailBase


class MailResetPassword(MailBase):
    name = 'Reset Password'
    subject = '__APPNAME__ password reset'
    template = 'email/reset_password.html'

    @classmethod
    def process(cls, user, data, request, **kwargs):
        reset_token = kwargs['reset_token']
        data = {
            'reset_url': settings.RESET_PASSWORD_URL.format(
                reset_token=reset_token,
                user_id=user.id
            ),
        }
        return data


class MailWelcomeUser(MailBase):
    name = 'Welcome User'
    subject = 'Welcome to __APPNAME__'
    template = 'email/welcome_user.html'

    @classmethod
    def process(cls, user, data, request, **kwargs):
        data = {
            'email': user.email,
        }
        return data
