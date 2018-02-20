release: python manage.py migrate
web: gunicorn project.wsgi --log-file=- --log-level=debug
worker: celery --app=project worker -l info --without-gossip --without-mingle --without-heartbeat --loglevel=debug
