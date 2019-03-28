# Add recipes to this file as needed

# From the command line:
# make <recipe-name>
# make erik-home-runserver
# make coverage

#Recipes
setup:
	pip install -r requirements.txt
	#create the database
	createdb django
	#create the user
	create user -s postgres
	#generate data tables
	python manage.py migrate
	#create the admin user
	python manage.py createsuperuser

erik-home-server:
	python manage.py runserver 192.168.1.90:8000

tests:
	python manage.py test apps

coverage:
	python manage.py test apps --with-coverage --cover-package=apps.user

localhost:
	python manage.py runserver
