from django.apps import AppConfig
from django.conf import settings
from django.core.checks import register, Warning
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist


class MailConfig(AppConfig):
    name = 'apps.mail'

    def ready(self):

        @register
        def template_check(app_configs, **kwargs):
            errors = []
            for mail_key in settings.MAIL_REGISTRY:
                try:
                    subject = settings.MAIL_REGISTRY[mail_key]['subject']
                except KeyError:
                    errors.append(
                        Warning(
                            "No subject field in settings.MAIL_REGISTRY['{}']".format(mail_key),
                            obj=settings,
                        )
                    )

                try:
                    template = settings.MAIL_REGISTRY[mail_key]['template']
                except KeyError:
                    errors.append(
                        Warning(
                            "No template field in settings.MAIL_REGISTRY['{}']".format(mail_key),
                            obj=settings,
                        )
                    )
                else:
                    try:
                        get_template(template)
                    except TemplateDoesNotExist:
                        errors.append(
                            Warning(
                                'Mail template "{}" not found'.format(template),
                                obj=settings,
                            )
                        )

            return errors
