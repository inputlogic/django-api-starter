from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cms.models.post import Post

from .libs import notify


@receiver(post_save, sender=Post, dispatch_uid='post_post_save_webhook')
def post_webhook_signal(sender, instance, created, **kwargs):
    """ Here's an example signal to trigger a webhook.

    If a Post is created, we notify our configured webhook url (see project/settings.py).
    For now, the notify function accepts two params: title and branch, as this can be passed
    to Netlify.

    Both params are optional with the following defaults:
        title: 'Triggered by Django signal'
        branch: 'master'
    """
    title = 'Triggered by new post' if created else 'Triggered by updated post'
    notify(title=title, branch='master')
