from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from djrichtextfield.models import RichTextField

from .base import AbstractContentType
from ..fields import ColorField


class Post(AbstractContentType):
    """
    Blog Post model based on "AbstractContentType".
    Any "Custom Post Type" should be built on "AbstractContentType" base class.

    AbstractContentType includes:
     - title
     - slug
     - tags
     - created_at
     - updated_at
    """
    published = models.BooleanField(default=False)
    published_on = models.DateTimeField(default=timezone.now)
    feature_image = models.ImageField(
        upload_to='feature_images', blank=True, null=False, default=''
    )
    feature_color = ColorField(_('Feature Color'), default='#000000', blank=True)
    body = RichTextField(blank=True)
