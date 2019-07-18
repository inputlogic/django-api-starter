# Django Mail

Email interface with static templates and logging.

## Usage

1. Define your mail interface in `mail.py` by subclassing `MailBase`.

2. Define `name`, `subject`, and `template` attributes on your mail interface.

`name` - Description of the type of mail message

`subject`- Django template string for the subject line

`template` - Path to a django template file for the body of the email

3. Add a `process(cls, user, data, request, **kwargs)` class method to process
your data and return a context that will be fed to your templates.

4. Create a django template for your email.

5. Call your subclass to create a new mail message and a task to send it.

## Example

Create mail interface:
`apps/barrowtrader/mail.py`
```python
class MailNewWheelbarrows(MailBase):
    name = 'New Wheelbarrows'
    subject = 'BarrowTrader | New wheelbarrow recommendations in the {{ city_name }} area!'
    template = 'email/new_wheelbarrows.html

    @classmethod
    def process(cls, user, data, request, **kwargs):
        data = {
          customer_name = user.name,
          city_name = kwargs['city_name'],
          wheelbarrows = kwargs['wheelbarrows'],
        }
        return data
```

Create mail template:
`apps/barrowtrader/templates/email/new_wheelbarrows.html`
```html
{% extends 'email/email_base.html' %}

{% block content %}
  <p>
    Hey {{ customer_name }}, check out these cool wheelbarrows to rent!
  </p>
  <ul>
    {% for barrow in wheelbarrows %}
      <li>{{ barrow.name }} - {{ barrow.description }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

Send mail:
`apps/barrowtrader/admin.py`
```python
...
if new_wheelbarrows != None:
    MailNewWheelbarrows(user, city_name=city.name, wheelbarrows=new_wheelbarrows)
...
```

See also `apps/user/mail.py` and `apps/user/templates/email/` for a working example of
project and template layout.
