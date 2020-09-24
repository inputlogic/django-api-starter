from django.contrib.auth import get_user_model
from django.db import models


class File(models.Model):
    IMAGE_MIME_TYPES = ('image/jpeg', 'image/png')

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='files')
    upload = models.FileField()
    mime_type = models.CharField(max_length=25)
    is_private = models.BooleanField(default=False)
    is_resized = models.BooleanField(default=False)  # for imagess
    is_verified = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.upload.url

    @property
    def is_image(self):
        return self.mime_type in File.IMAGE_MIME_TYPES

    def delete(self, *args, **kwargs):
        """ Delete the actual file, when the model instance is deleted.

        See: https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.fields.files.FieldFile.delete
        """
        if self.upload:
            self.upload.delete()
        super().delete(*args, **kwargs)
