from unittest.mock import patch

from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from apps.user.models import User


class PublicSignupTests(APITestCase):
    @patch('apps.mail.models.Mail.send')
    def test_register_user(self, mock_send):
        """
        Ensure we can register a new user object.
        """
        url = reverse('public-user-signup')
        data = {'email': 'test@example.org', 'password': 'yayhooray'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email,
                         'test@example.org')

    @patch('apps.mail.models.Mail.send')
    def test_register_user_icase(self, mock_send):
        """
        User emails should be stored in lowercase
        """
        url = reverse('public-user-signup')
        email = 'uppercaseLOWERCASE@lowercaseUPPERCASE.ca'
        data = {'email': email, 'password': 'yayhooray'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(
            get_user_model().objects.get().email,
            email.lower()
        )

    def test_exiting_user(self):
        url = reverse('public-user-signup')
        user = mixer.blend(User)
        data = {'email': user.email, 'password': 'yayhooray'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
