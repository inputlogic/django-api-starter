# Django Mail

Django app to manage email templates and sending via the admin interface.

## Usage Details

1. Define your mail templates via the Django Admin.
2. We recommend adding a `mails.py` file for each app, to wrap your `Mail.send` calls in functions.
3. Use those functions wherever you wish to trigger those emails.

## Example

We ship [fixtures for two default emails](https://github.com/inputlogic/django-api-starter/blob/master/mail-templates.json) to be used by the `user` app. Once you have a template defined, you can trigger sending a mail using that template via the `Mail.send` static method:

```python
Mail.send('WelcomeUser', user)
```

[Example `mails.py`](https://github.com/inputlogic/django-api-starter/blob/master/apps/user/mail.py) for the user app.

## Improving Template Management

For now you are limited to the [fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/) feature of Django to move templates from local development to staging or production servers.

We have an [open issue](https://github.com/inputlogic/django-api-starter/issues/91) to discuss tools and potential new features to improve this processs.
