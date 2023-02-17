# Run on host (your) machine
build:
	docker compose build

run:
	docker compose up

restart:
	docker compose restart

stop:
	docker compose down

shell:
	docker exec -it django-api-starter-web-1 /bin/bash


# Run on docker instance (run `make shell` first)
lint:
	python -m flake8 --ignore E501,E722,F821,W504 apps/ project/ libs/

test:
	python manage.py test apps

coverage:
	python manage.py test apps --with-coverage --cover-package=apps.user
