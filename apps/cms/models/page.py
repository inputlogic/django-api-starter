from django.db import models

from djrichtextfield.models import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

from .base import SlugBase, AbstractMetadata


class Page(SlugBase, AbstractMetadata, MPTTModel):
    LAYOUT_CHOICES = (
        ('simple', 'Simple'),
        ('sectioned', 'Sectioned'),
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE
    )
    sub_title = models.CharField(max_length=255)
    layout = models.CharField(choices=LAYOUT_CHOICES, default='simple', max_length=30)
    body = RichTextField(null=True, blank=True)
    sidebar = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ('title',)


class Section(models.Model):
    page = models.ForeignKey('cms.Page', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='section_images')
    body = RichTextField(null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
