release: python manage.py migrate
web: gunicorn project.wsgi -c python:project.gunicorn
worker: python manage.py runworkers
