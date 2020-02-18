from django.contrib.auth import get_user_model
from django.db import models

from .tasks import update_salesforce_device_id


class Firebase(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='firebase_devices'
    )
    registration_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'registration_id')

    def __str__(self):
        return '{0} - {1}'.format(self.user.email, self.registration_id)

