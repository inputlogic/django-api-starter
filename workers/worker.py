import json
from django.utils import timezone

from .models import Task


registry = {}  # Store reference to task functions
scheduled = []  # Scheduled tasks to be started on `runworkers` cmd


def task(schedule=None):
    def task_handler(fn):
        handler = '{0}.{1}'.format(fn.__module__, fn.__name__)
        registry[handler] = fn

        if schedule:
            scheduled.append({'handler': handler, 'schedule': schedule})

        def wrapper(*args, **kwargs):
            Task.objects.create(
                handler=handler,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                run_at=timezone.now(),
            )
        return wrapper
    return task_handler
