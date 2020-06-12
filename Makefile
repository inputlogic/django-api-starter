# Add recipes to this file as needed

# From the command line:
# make <recipe-name>
# make erik-home-runserver
# make coverage

setup:
	pip install -r requirements.txt
	python manage.py migrate

erik-home-server:
	python manage.py runserver 192.168.1.90:8000

tests:
	python manage.py test apps

coverage:
	python manage.py test apps --with-coverage --cover-package=apps.user

localhost:
	python manage.py runserver
