import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from libs.instagram import InstagramError
from .instagram import InstagramInfo


log = logging.getLogger(__name__)


class SocialAuth(models.Model):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    PROVIDERS = (
        (FACEBOOK, _(FACEBOOK)),
        (GOOGLE, _(GOOGLE)),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    social_id = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=300, blank=True)
    details = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('social_id', 'provider',)

    def __str__(self):
        return '<SocialAuth: {}>'.format(self.user)

    @staticmethod
    def login_or_signup(provider, access_token, info):
        """ Log in or Sign up user

        Returns a tuple:
            (social_auth, user_created)
        """
        social_id = str(info['id'])
        email = info.get('email')

        try:
            social_auth = SocialAuth.objects.get(provider=provider, social_id=social_id)
            social_auth.token = access_token
            social_auth.details = info
            social_auth.save()
            return social_auth, False
        except SocialAuth.DoesNotExist:
            # If signing up a new user, we need an email address
            if not email:
                raise ValidationError(
                    "We couldn't get the email associated with that facebook account.")
            
            user, user_created = get_user_model().objects.get_or_create(email=email)
            social_auth, _ = SocialAuth.objects.update_or_create(
                provider=provider,
                social_id=social_id,
                defaults={
                    'token': access_token,
                    'user': user,
                    'details': info,
                }
            )
            return social_auth, user_created
