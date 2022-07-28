import importlib
import inspect
import json
import logging
from functools import wraps

from django.utils import timezone

from . import registry
from inspect import getcallargs

log = logging.getLogger(__name__)


def run_now(handler, *args, **kwargs):
    try:
        module_path, function_name = handler.rsplit('.', 1)
        module = importlib.import_module(module_path)
        fn = getattr(module, function_name)
        results = fn.__wrapped__(*args, **kwargs)
        return results
    except Exception as e:
        log.exception(e)


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

            if kwargs.pop('now', False):
                call_args = inspect.getcallargs(f, *args, **kwargs)
                return run_now(path, *args, **kwargs)
            else:
                from .models import Task
                Task.objects.get_or_create(
                    handler=path,
                    args=json.dumps(args),
                    kwargs=json.dumps(kwargs),
                    run_at=run_at_time,
                    status=Task.WAITING
                )
        return wrapper
    return handler
