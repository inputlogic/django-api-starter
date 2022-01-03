# Django API Starter

## Versions
- Python 3.8.12
- Django 4.0

## Installation

Create and activate local python environment:

```
virtualenv env
. ./env/bin/activate
```

Create database:
```
createdb ___PROJNAME___
```

Change database name in `project/settings.py` to match the one you just created:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django', # ___CHANGEME___
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    },
}
```

Setup & run Django:
```
make setup
./manage.py createsuperuser
./manage.py runserver
```

A note on `requirements.init.txt` vs `requirements.txt`:

> `requirements.init.txt` installs the latest versions of each package.
>
> If you have problems with the packages installed from `requirements.init.txt`,
> try installing django-api-starter's `requirements.txt` instead. It contains
> specific versions that are expected to work.

