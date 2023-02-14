setup:
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata fixtures/admin.json
	python manage.py loaddata fixtures/mail.json

lint:
	python -m flake8 --ignore E501,E722,F821,W504 apps/ project/ libs/

tests:
	python manage.py test apps

coverage:
	python manage.py test apps --with-coverage --cover-package=apps.user

run:
	python manage.py runserver_plus

shell:
	docker exec -it <web-container-name> /bin/bash
