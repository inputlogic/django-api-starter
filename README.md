# Django API Starter

## Versions
- Python 3.11.x
- Django 4.1.x

## Docker Setup

1. Install Docker.
2. Run `docker compose up`.
3. Profit.

If you'd like to run commands like `./manage.py <command>` on the Docker instance, connect to
the web shell.

First update the `Makefile` to match your web container name in the `shell` command and run:

```
$ make shell
```

## Manual Setup

1. Setup a virtual environment and activate.

```
$ virtualenv env
$ . env/bin/activate
(env) $
```

2. Create Postgres database.
```
(env) $ createdb django
```

3. Install Django dependencies and build database.
```
(env) $ make setup
```

4. Run the project (using improved dev server).
```
(env) $ make run
```
