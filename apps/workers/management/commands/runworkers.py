from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start workers and wait for tasks to process'

    def handle(self, *args, **options):
        # Load all tasks.py so we can get `scheduled` tasks
        from ... import util
        util.autodiscover()

        # Add scheduled tasks to the queue
        from ... import registry
        scheduled = registry.get()
        if scheduled:
            from ...models import Task
            for handler, schedule, run_at in scheduled:
                Task.create_scheduled_task(handler, schedule, run_at)

        # Close active db connection so workers create their own
        # This is REQUIRED for multiprocessing to work with Django
        from django import db
        db.connections.close_all()

        # Startup workers and run until killed
        from ... import consumer
        consumer.run_forever()
