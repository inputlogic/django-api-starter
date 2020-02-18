from importlib import import_module
import inspect

from django.apps import AppConfig, apps as django_apps
from django.core.checks import register, Warning
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist


class MailConfig(AppConfig):
    name = 'apps.mail'

    def ready(self):

        @register
        def mailbase_check(app_configs, **kwargs):
            from .base import MailBase
            errors = []

            for app_config in django_apps.get_app_configs():
                try:
                    mail_module = import_module('{}.mail'.format(app_config.name))
                    for name, obj in inspect.getmembers(mail_module):
                        if inspect.isclass(obj) and obj is not MailBase and issubclass(obj, MailBase):
                            try:
                                get_template(obj.get_template())
                            except TemplateDoesNotExist:
                                errors.append(
                                    Warning(
                                        'Mail template not found at "{}"'.format(
                                            obj.get_template()
                                        ),
                                        obj=obj,
                                    )
                                )
                except ModuleNotFoundError:
                    pass

            return errors
