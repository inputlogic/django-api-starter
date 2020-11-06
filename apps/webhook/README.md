# Webhook App

This app is for notifying webhooks when certain models are saved. The primary use-case, is to trigger Netlify deploys when certain models are created/updated. That way, the front-end will refresh it's API requests cache for faster loading when visited.

For now, the app is very simple, and requires configuration via code. If the use-cases or needs of this app expand, it could be modified to allow configuration via the Django admin.

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
3. Copy the URL and add it as an environment variable, `WEBHOOKS_NOTIFY_URL`
4. Edit `apps/webhook/signals.py` to configure when to notify the webhook
