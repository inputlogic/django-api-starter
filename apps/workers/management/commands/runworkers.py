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
            for handler, schedule in scheduled:
                Task.create_scheduled_task(handler, schedule)

        # Startup workers and run until killed
        from ... import consumer
        consumer.run_forever()
