# Django Firebase App

Track user devices in a Firebase table and expose a task for triggering push
notifications.

## Installation

Add it to your Django installed apps:

```python
INSTALLED_APPS = [
    # ...
    'apps.firebase',
    # ...
]
```

Add the firebase urls to your project:

```python
urlpatterns = [
    # ...
    url(r'^', include('apps.firebase.urls')),
    # ...
]

### Setup Firebase

1. Create a new Firebase project: [https://console.firebase.google.com](https://console.firebase.google.com) 
2. Add the [firebase-admin](https://pypi.org/project/firebase-admin/) to your
`requirements.txt`.
3. [Generate a private key
   file](https://firebase.google.com/docs/admin/setup?authuser=0#initialize-sdk)
4. Add the generated JSON file to the root of your Django project.
5. Set `GOOGLE_APPLICATION_CREDENTIALS` in your `settings.py` file. Ex. value: `'django-example-firebase-adminsdk-PA6ejnBU.json'`

### Example Code

```python
from apps.firebase.libs import send_notification
from apps.firebase.models import Firebase

# ...

devices = Firebase.objects.filter(user=user)

if devices:
    for device in devices:
        send_notification(device.registration_id, {
            'title': 'My Cool Notification!',
            'body': 'Hey "{}"!'.format(user.full_name)
        })
```
