from datetime import datetime

from apps.workers import task


#  @task()
def say_hello(name):
    """
    Example of a 'one-off' task that can be called anywhere in you code by importing it.

    """
    print('Hello', name)


#  @task()
def failing_task():
    """
    Example of how failed tasks work (they're logged in admin)

    """
    raise Exception('task failed :(')


#  @task(schedule=10)
def say_hello_every_10_seconds():
    """
    Example repeating task that will run every 10 seconds based on the `schedule` param.

    Can also be called directly.

    """
    print('Howdy, its', datetime.utcnow())


#  @task(schedule=30)
def say_hello_every_30_seconds():
    """
    Example repeating task that will run every 30 seconds based on the `schedule` param.

    Can also be called directly.

    """
    print('Oh hai, its', datetime.utcnow())


@task(schedule=10)
def long_running_task():
    print('start of long running task')
    import time
    time.sleep(30)
    print('end of long running task')
