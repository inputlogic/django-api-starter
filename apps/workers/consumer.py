import os
import json
import logging
import signal
import time
import importlib
from multiprocessing import get_context

from django.db import transaction
from django.utils import timezone

import django
django.setup()

from .models import Task  # noqa: E402
from .settings import SLEEP, KEEP  # noqa: E402


log = logging.getLogger(__name__)


def init_pool():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def process_task(task_id, handler, args, kwargs):
    log.debug(f'[{os.getpid()}] started task {task_id}')
    success = False
    error = 'Task failed without error.'

    try:
        module_path, function_name = handler.rsplit('.', 1)
        module = importlib.import_module(module_path)
        fn = getattr(module, function_name)
        args = json.loads(args)
        kwargs = json.loads(kwargs)

        fn.__wrapped__(*args, **kwargs)
        success = True
        error = ''
    except Exception as e:
        log.exception(e)
        success = False
        error = str(e)

    log.debug(f'[{os.getpid()}] finished task {task_id} ({success}, {error})')
    return task_id, success, error


def purge_tasks():
    """
    Removes completed tasks greater than settings.KEEP.

    """
    tasks = Task.objects.exclude(completed_at=None).all()
    Task.objects.filter(id__in=tasks).exclude(id__in=tasks[:KEEP]).delete()


def handle_callback(result):
    """
    Triggered by `pool.apply_async` callback, given result status (str) of the task.

    """
    (task_id, success, error) = result
    task = Task.objects.get(pk=task_id)
    task.status = Task.COMPLETED if success else Task.FAILED
    task.error = error
    task.completed_at = timezone.now()
    task.save()

    if task.schedule:
        Task.create_scheduled_task(task.handler, task.schedule)


def run_forever():
    try:
        with get_context("spawn").Pool(initializer=init_pool, maxtasksperchild=1) as pool:
            while True:
                with transaction.atomic():
                    task = (
                        Task.objects
                        .select_for_update()
                        .filter(run_at__lte=timezone.now())
                        .filter(status=Task.WAITING)
                        .first()
                    )

                    if task:
                        task.status = Task.RUNNING
                        task.save()
                        pool.apply_async(
                            process_task,
                            args=(task.id, task.handler, task.args, task.kwargs),
                            callback=handle_callback
                        )
                    else:
                        purge_tasks()  # If we have a sec, cleanup old tasks
                        time.sleep(SLEEP)
                    log.debug('waiting for tasks...')

    except (KeyboardInterrupt, SystemExit):
        log.debug('workers stopped, waiting for lingering tasks...')
        pool.close()
        pool.join()
    finally:
        (Task.objects
            .filter(status=Task.RUNNING)
            .update(status=Task.INCOMPLETE, error='Worker shutdown prematurely.'))
