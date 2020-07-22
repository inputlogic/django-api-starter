import factory
from django.utils.text import slugify

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
