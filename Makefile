setup:
	pip install -r requirements.init.txt
	#create the database
	createdb django
	#create the user
	createuser -s postgres
	#generate data tables
	python manage.py migrate
	#create the admin user
	python manage.py createsuperuser

run-tests:
	python manage.py test apps

run-coverage:
		python manage.py test apps --with-coverage --cover-package=apps.content,apps.user,apps.workerexample

localhost:
	python manage.py runserver
