# Django Mail

Email interface with static templates and logging.

## Usage

1. Define your mail interface in `mail.py` by subclassing `MailBase`.

2. Create a Django template for your email.

3. **[Optional]** Add a `process_args(cls, user, request, *args, **kwargs)` class
   method to process your data and return a context dict that will be fed to your
   templates.

   By default, `user`, `request`, and the contents of `**kwargs` will be passed
   directly from `send()` to your templates as a dict.

4. **[Optional]** Define `name`, `subject`, and `template` attributes on your mail
   interface.

   **`name`**: Description of the type of mail message. Defaults to the interface's
   class name (minus 'Mail' if present at the front).

   **`subject`**: Django *template string* for the subject line. Defaults to the `name`
   attribute of the class.

   **`template`**: Path to a Django *template file* for the body of the email. Defaults to
   `email/name_attribute.html`, where `name_attribute.html` is the snake_case version
   of the `name` attribute, plus `.html`.

   If you need these attributes to be dynamic, you can override the class methods
   `get_name()`, `get_subject()`, and `get_template()` instead -- for instance, to
   get a user-editable template from a custom model.

5. Call `.send(user, request, admin_feedback, *args, **kwargs)` on your subclass to
   create a new mail message and a task to send it to the email associated with
   `user`.

   If you are generating emails inside the Django admin, you can pass in the `request`
   object and set `admin_feedback=True` to generate a notification that the mail
   has been created and is awaiting delivery.

## Example

### Create mail template:

This is a standard Django template. The variables come from the dict returned by
`process_args()`.

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

### Create mail interface:

Subclass `MailBase` and define the properties you want to customize.

`apps/barrowtrader/mail.py`
```python
class MailNewWheelbarrows(MailBase):
    name = 'New Wheelbarrows'
    subject = 'BarrowTrader | New wheelbarrow recommendations in the {{ city_name }} area!'
    template = 'email/new_wheelbarrows.html

    @classmethod
    def process_args(cls, user, request, *args, **kwargs):
        ctx = {
          'customer_name': user.name,
          'city_name': kwargs['city_name'],
          'wheelbarrows': kwargs['wheelbarrows'],
        }
        return ctx
```

Note that in this example, the `template` attribute is actually redundant!

Because the `name` is 'New Wheelbarrows', the class will automatically look for a
template at the path 'email/new_wheelbarrows.html'. Doesn't hurt to be specific,
though.

### Send mail:

Call `send()` on your class.

`apps/barrowtrader/admin.py`
```python
...
if new_wheelbarrows is not None:
    MailNewWheelbarrows.send(user, city_name=city.name, wheelbarrows=new_wheelbarrows)
...
```

See also `apps/user/mail.py` and `apps/user/templates/email/` for a working example of
project and template layout.
