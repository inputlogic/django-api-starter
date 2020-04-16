from django.db import models
from django.utils.text import slugify

from djrichtextfield.models import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


class SlugBase(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Page.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Tag(SlugBase):
    pass


# Pages


class Page(SlugBase, MPTTModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE
    )
    body = RichTextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ('title',)


class Section(models.Model):
    page = models.ForeignKey('cms.Page', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='section_images')
    body = RichTextField(null=True)
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['sort_order']


# Posts


class Post(SlugBase):
    body = RichTextField(null=True)
    tags = models.ManyToManyField('cms.Tag', related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Work(Post):
    """
    Example 'Custom Post Type'
    """
    headline = models.CharField(max_length=255, null=True, blank=True)
    intro_image = models.ImageField(upload_to='intro_images')
    intro_body = RichTextField(null=True)


class Slide(models.Model):
    work = models.ForeignKey('cms.Work', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='slide_images')
    body = RichTextField(null=True)
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['sort_order']
