from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def test_register_user(self):
        """
        Ensure we can register a new user object.
        """
        url = reverse('signup')
        data = {'email': 'test@example.org', 'password': 'yayhooray'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, 'test@example.org')

    def test_get_profile(self):
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',)
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('me'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
