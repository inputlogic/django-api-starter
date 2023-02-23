import logging
from celery import shared_task


log = logging.getLogger(__name__)


@shared_task()
def example_success(name):
    log.debug('Hello, ' + name)


@shared_task()
def example_fail():
    raise Exception('Im a failed task :(')


@shared_task()
def example_scheduled_task():
    log.debug('Im called from the schedule!')
