# Django API Starter

## Requirements
- Docker

## Versions
- Python 3.11.x
- Django 4.1.x

## Local Development

To run the project, do:

```
$ make run
```
This will handle building the initial image and starting the project. If you change any system
level files like `requirements.txt` make sure you re-build the image with:

```
$ make build
```

If you want to run commands on the container such as `./manage.py <command>`, do:

```
$ make shell
```

This will open a bash shell on the web container. 
