from datetime import datetime

from workers import task


@task()
def say_hello(name):
    """
    Example of a 'one-off' task that can be called anywhere in you code by importing it.

    """
    print('Hello', name)


@task(schedule=30)
def say_hello_every_30_seconds():
    """
    Example repeating task that will run every 30 seconds based on the `schedule` param.

    Can also be called directly.

    """
    print('Hey, its', datetime.utcnow())
