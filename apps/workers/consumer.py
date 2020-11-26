import os
import json
import logging
import signal
import time
import importlib
from multiprocessing import Pool

from django.db import transaction
from django.utils import timezone

import django
django.setup()

from .models import Task
from .settings import SLEEP, PURGE


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

    log.debug('[{0}] running task id {1}: {2}'.format(os.getpid(), task.id, task.handler))

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


#  def purge_tasks():
#      # EX: if PURGE is 1000, we will keep the latest 1000 completed tasks
#      keep = (
#          Task.objects
#          .filter(status=Task.COMPLETED)
#          .order_by('-completed_at')
#          .order_by('-run_at')[:PURGE]
#      )
#
#      if keep:
#          # If there are more than PURGE (ex. 1000) completed tasks, delete
#          # any that are not in keep
#          Task.objects.exclude(pk__in=keep).filter(status=Task.COMPLETED).delete()


def run_forever():
    try:
        pool = Pool(initializer=init_pool)
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
                    pool.apply_async(process_task, args=(task.id,))
                else:
                    time.sleep(SLEEP)
    except (KeyboardInterrupt, SystemExit):
        log.debug('workers stopped, waiting for lingering tasks...')
        pool.close()
        pool.join()
