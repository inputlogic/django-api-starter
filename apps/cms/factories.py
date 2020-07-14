import factory
from django.utils.text import slugify

from .models.post import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'Post {}'.format(n))
    slug = factory.LazyAttribute(lambda post: slugify(post.title)) 
