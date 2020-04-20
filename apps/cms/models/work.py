from django.db import models

from djrichtextfield.models import RichTextField

from .base import AbstractContentType


class Work(AbstractContentType):
    """
    Example 'Custom Post Type'
    """
    headline = models.CharField(max_length=255, null=True, blank=True)
    intro_image = models.ImageField(upload_to='intro_images')
    intro_body = RichTextField(null=True)

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Work'


class Slide(models.Model):
    work = models.ForeignKey('cms.Work', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='slide_images')
    body = RichTextField(null=True)
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['sort_order']
