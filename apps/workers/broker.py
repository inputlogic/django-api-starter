import json
from functools import wraps

from django.utils import timezone

from . import registry


def task(schedule=None):
    def handler(f):
        path = '{0}.{1}'.format(f.__module__, f.__name__)

        if schedule:
            registry.add(path, schedule)

        @wraps(f)
        def wrapper(*args, **kwargs):
            run_at = kwargs.pop('_schedule', timezone.now())
            from .models import Task
            Task.objects.create(
                handler=path,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                run_at=run_at,
            )
        return wrapper
    return handler
