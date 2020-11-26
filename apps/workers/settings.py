from django.conf import settings


# How long (in seconds) should the worker sleep between task lookups?
SLEEP = getattr(settings, 'WORKERS_SLEEP', 5)

# How many logs to keep in admin
KEEP = getattr(settings, 'WORKERS_KEEP', 100)
