from django.db import models

class Content(models.Model):
    identifier = models.CharField(max_length=255)
    page = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        unique_together = (('identifier', 'page'),)
