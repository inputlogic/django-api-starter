import json
from functools import wraps

from django.utils import timezone

from . import registry


def task(schedule=None, run_at=timezone.now()):
    def handler(f):
        path = '{0}.{1}'.format(f.__module__, f.__name__)

        if schedule:
            registry.add(path, schedule, run_at)

        @wraps(f)
        def wrapper(*args, **kwargs):
            kwargs_run_at = kwargs.pop('_schedule', None)
            if kwargs_run_at:
                run_at_time = kwargs_run_at
            else:
                run_at_time = run_at
            from .models import Task
            Task.objects.get_or_create(
                handler=path,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                run_at=run_at_time,
            )
        return wrapper
    return handler
