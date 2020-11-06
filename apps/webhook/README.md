# Webhook App

This app is for configuring webhooks to hit based on certain Django events. For example, hitting a webhook when new data is saved.

Usage
-----

1. Add it to your Django installed apps:
```python
INSTALLED_APPS = [
    # ...
    'apps.webhook',
    # ...
]
```
2. Add a build hook on your Netlify project ([Netlify docs](https://docs.netlify.com/configure-builds/build-hooks/#parameters))
3. Copy the URL and add it via the Django admin `admin/webhook/webhook`
