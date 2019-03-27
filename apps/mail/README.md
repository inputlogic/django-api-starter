# Django Mail

Email interface with static templates and logging.

## Setup

Define your emails in settings.MAIL_REGISTRY.

Each email has a subject template string and a body template path. By convention,
email templates are stored in `templates/email/` for each particular app. Both
the subject string and the body template use the standard Django templating
engine for rendering.

Email templates can extend `templates/email/email_base.html` for project-wide
styling and layout.

## Usage

Create your mail interface functions in `mail.py` in your app directory. Process
any data here and call `Mail.send` to generate a task to send that mail.

Note that if you are sending mail from the Django Admin, you can pass a `request`
object to `Mail.send` to generate a message that the mail was sent.

## Example

See `apps/user/mail.py` and `apps/user/templates/email/` for a typical example of
project and template layout.

Register your email type, subject string and template path in settings:

`project/settings.py`
```python
MAIL_KEY_PASSWORD = 'Reset Password'
MAIL_REGISTRY = {
    MAIL_KEY_PASSWORD: {
        'subject': 'Password reset',
        'template': 'email/reset_password.html',
    },
}
```

Create the template file:

`apps/user/templates/email/reset_password.html`
```html
{% extends 'email/email_base.html' %}

{% block content %}
<p>
  Visit <a href='{{ reset_url }}'/>{{ reset_url }}</a> to reset your password.
</p>
{% endblock %}
```

Create a `mail.py` module in your app that defines your mail interface and
preprocesses the data you wish to send with `Mail.send`:

`apps/user/mail.py`
```python
def mail_reset_password(user, reset_token, request=None):
    reset_url = settings.RESET_PASSWORD_URL.format(
        reset_token=reset_token,
        user_id=user.id
    )
    return Mail.send(
        settings.MAIL_KEY_PASSWORD,
        user,
        {
          'reset_url': reset_url
        },
        request
    )
```

Then call `mail_reset_password(user, reset_token, request)` to send a password
reset email.
