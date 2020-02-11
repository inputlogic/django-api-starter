from django.conf import settings

from ..mail.base import MailBase


class MailResetPassword(MailBase):
    name = 'Reset Password'
    subject = '__APPNAME__ password reset'
    template = 'email/reset_password.html'

    @classmethod
    def process_args(cls, user, request, **kwargs):
        reset_token = kwargs['reset_token']
        ctx = {
            'reset_url': settings.RESET_PASSWORD_URL.format(
                reset_token=reset_token,
                user_id=user.id
            ),
        }
        return ctx


class MailWelcomeUser(MailBase):
    name = 'Welcome User'
    subject = 'Welcome to __APPNAME__'
    template = 'email/welcome_user.html'

    @classmethod
    def process_args(cls, user, request, **kwargs):
        ctx = {
            'email': user.email,
        }
        return ctx
