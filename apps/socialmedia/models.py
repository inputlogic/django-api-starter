from django.db import models

from project import settings


class SocialMedia(models.Model):
    FACEBOOK = 0
    GOOGLE = 1
    SOCIAL_MEDIA_SOURCES = (
        (0, 'Facebook'),
        (1, 'Google')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        related_name='social_media',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    source = models.IntegerField(choices=SOCIAL_MEDIA_SOURCES, db_index=True, default=FACEBOOK)
    identifier = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.identifier

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'
        unique_together = (('user', 'source', 'identifier'),)
