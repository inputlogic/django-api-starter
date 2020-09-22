from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import PostFactory


class PostTests(APITestCase):
    def setUp(self):
        self.post = PostFactory()

    def test_post_by_slug(self):
        url = reverse('post-by-slug', args=(self.post.slug,))
        response = self.client.get(url, format='json')
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('body', response.data)
        self.assertIn('published_on', response.data)
