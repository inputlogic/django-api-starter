# Django API Starter

## Installation

Clone repo:
```
git clone https://github.com/inputlogic/django-api-starter.git ___PROJNAME___
cd __PROJNAME__
```

Create and activate local python environment:
```
virtualenv env
. ./env/bin/activate
```

Install requirements:

```
pip install -r requirements.init.txt
pip freeze > requirements.txt
rm requirements.init.txt
```

A note on `requirements.init.txt` vs `requirement.txt`:

> `requirement.init.txt` installs the latest versions of each package.
>
> If you have problems with the packages installed from `requirements.init.txt`,
> try installing django-api-starter's `requirements.txt` instead. It contains
> specific versions that are expected to work.

Save local environment variables:

```
mv env.template .env
```

Create database:
```
createdb ___PROJNAME___
```

Find and change project-specific placeholders:
```
project/settings.py:97
```

Delete workerexample app:
```
rm -rf apps/workerexample
project/settings.py:55
project/urls.py:19
```

Django setup:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

Create a fresh git repo for the new project:
```
rm -rf .git
git init
git commit -am '___PROJNAME___ initial commit from django-api-starter'
```