from django.contrib.auth import get_user_model
from django.db import models


class File(models.Model):
    '''
    This model is used to keep track of files uploaded to s3.
    By associating files with the user that created them it can be used
    to prevent unaccepted use of file uploading.

    The verified field shows whether it has been verified that a file
    was uploaded at the url. (Since the file should be made when the
    signed s3 url is sent to the client, there can be instances where
    no file actually gets uploaded to s3.)
    '''
    IMAGE_MIME_TYPES = ('image/jpeg', 'image/png')

    link = models.URLField(unique=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='files'
    )
    is_private = models.BooleanField(default=False)
    is_resized = models.BooleanField(default=False, db_index=True)  # Only if mime type is image
    mime_type = models.CharField(max_length=25, db_index=True)
    verified = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link.split('/')[-1]

    @property
    def owner(self):
        return self.user

    @property
    def is_image(self):
        return self.mime_type in File.IMAGE_MIME_TYPES

    @classmethod
    def images_to_resize(cls):
        """
        Get all image File's that haven't been marked as resized.

        """
        return cls.objects.filter(
            mime_type__in=File.IMAGE_MIME_TYPES,
            is_resized=False,
            is_private=False).all()
