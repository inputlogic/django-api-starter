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


def process_task(task_id):
    task = Task.objects.get(id=task_id)
    module_path, function_name = task.handler.rsplit('.', 1)
    module = importlib.import_module(module_path)
    fn = getattr(module, function_name)
    args = json.loads(task.args)
    kwargs = json.loads(task.kwargs)

    log.debug(f'running task({task.id}): {task.handler}')

    try:
        fn.__wrapped__(*args, **kwargs)
        task.status = Task.COMPLETED
    except Exception as e:
        task.status = Task.FAILED
        task.error = str(e)
        log.exception(e)

    task.completed_at = timezone.now()
    task.save()

    if task.schedule:
        Task.create_scheduled_task(task.handler, task.schedule)

    return task_id


def purge_tasks():
    """
    Removes completed tasks greater than settings.KEEP.

    """
    tasks = Task.objects.exclude(completed_at=None).all()
    Task.objects.filter(id__in=tasks).exclude(id__in=tasks[:KEEP]).delete()


def run_forever():
    try:
        with get_context("spawn").Pool(initializer=init_pool, maxtasksperchild=1) as pool:
            running = []
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
                        running.append(task.id)
                        pool.apply_async(
                            process_task,
                            args=(task.id,),
                            callback=lambda task_id: running.remove(task_id)
                        )
                    else:
                        purge_tasks()  # If we have a sec, cleanup old tasks
                        time.sleep(SLEEP)
                    log.debug(f'running tasks: {running}')
    except (KeyboardInterrupt, SystemExit):
        log.debug('workers stopped, waiting for lingering tasks...')
        pool.close()
        pool.join()
    finally:
        res = Task.objects.filter(id__in=running).update(status=Task.INCOMPLETE, error='Worker shutdown prematurely.')
        log.debug(f'incomplete tasks: {res}')
