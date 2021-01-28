# Django Workers

A simple background task worker that uses your Django database and admin for management. This
project is meant for small to medium scale uses. If you need something more, check out Celery.


## Install

Add it to your Django installed apps

```python
INSTALLED_APPS = [
    # ...
    'apps.workers',
    # ...
]
```

## Basics

Create a `tasks.py` file in the Django app you'd like to have tasks in. These tasks will automatically
become available thanks to autodiscovery.

```python
from apps.workers import task

@task()
def say_hello(name):
    print('Howdy', name)
```

### Calling tasks

Tasks become simple Python callables. Calling them inserts that task to your Django database and
waits for a worker to pick it up.

```python
say_hello('Foo')  # Sent to background automatically
```

### Running the workers

Now boot-up your workers to crunch some data. Workers poll the Database for new tasks they should
work on.

```
python manage.py runworkers
```


## Scheduled tasks

Sometimes you want to run a specific task every X seconds or at a later date. Thats what scheduled 
tasks are for.

### Repeating scheduled tasks

Tasks specified with a schedule in seconds will repeat. Note that a scheduled task is only added 
back into the queue after it completes (or fails).

```python
from workers import task

@task(schedule=10)
def do_something():
    print('I run every 10 seconds')

@task(schedule=60*5)
def do_something_later():
    print('I run every 5 minutes')

@task(schedule=60*60*8)
def do_something_even_later():
    print('I run every 8 hours')
```

### Date scheduled tasks

Tasks can be scheduled to *run once* at a later date by passing a `_schedule=<datetime>` argument 
when the task is called.

```python
from datetime import datetime, timedelta
from workers import task

trial_end_date = datetime.utcnow() + timedelta(days=14)

@task()
def trial_ending():
    send_email('Your trial is ending!')

# Specifying the `schedule` argument will tell the worker when this task should run
trial_ending(_schedule=trial_end_date)


## Concurrency

Workers are run in a multiprocessing pool equal to the number of cores available. This happens
automatically. Additionally, you may run multiple versions of `./manage runworkers` (on two
different servers for example) without the worry of race conditions.
```

## Settings

You can optionally override these settings in your Django `settings.py` file:

- `WORKERS_SLEEP` (default 5) - If no tasks were in the queue, wait a number of seconds before checking again.
- `WORKERS_KEEP` (default 100) - How many recent task logs to keep in the admin

#### TODO (not working)

- `WORKERS_TIMEOUT` (default 30) - Seconds a task can run before its killed
- `WORKERS_RETRY` (default 3) - Number of retries before giving up
