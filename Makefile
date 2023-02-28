# Try to determine dir name so we don't need to manually set docker instance names below
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

build:
	docker compose build

run:
	docker compose up

restart:
	docker compose restart

stop:
	docker compose down

shell:
	docker exec -it ${current_dir}-web-1 /bin/bash

psql:
	docker exec -it ${current_dir}-db-1 psql -U postgres postgres

lint:
	docker exec -it ${current_dir}-web-1 python -m flake8 --ignore E501,E722,F821,W504 apps/ project/ libs/

test:
	docker exec -it ${current_dir}-web-1 python manage.py test apps
