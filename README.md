Django API Starter
=================


Requirements
------------
- [Docker (Desktop)](https://www.docker.com/products/docker-desktop/)


Versions
--------
- Python 3.11.x
- Django 4.1.x
- Postgres 15.x


Local Development
-----------------

To run the project via Docker, do:

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


Integrations
------------
This section is meant to detail integrations used on a project as well as their purpose.

- [Postmark](https://postmarkapp.com) for sending emails.
- [Firebase](https://firebase.google.com) for sending push notifications to mobile.
- [Sentry](https://sentry.io) for tracking Django errors.
- [Stripe](https://stripe.com) for handling payments.


Additional
----------
This section is meant for project-specific logic. Ideally, each of these are linked to a [Loom](https://www.loom.com) video walking through the implemention.

### Stripe
We use Stripe's subscription model to bill clients on a monthly or annual basis. Each plan includes a 14 day free trail. 

- [Loom walkthrough](https://loom.com)
- All payment logic is stored on stripe
- Our database only stores client and subscription ids, nothing else
- All payment logic is handled via [webhooks](https://stripe.com/docs/billing/subscriptions/webhooks)
