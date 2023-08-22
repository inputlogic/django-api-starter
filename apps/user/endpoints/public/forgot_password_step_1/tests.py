from unittest.mock import patch
from urllib.parse import urlparse

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class ForgotPasswordStep1Tests(APITestCase):

    @patch('apps.mail.models.Mail.send')
    def test_user_can_reset_password(self, mock_send):
        new_password = 'whatever'
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',)
        response = self.client.post(
            reverse('public-user-forgot-password-step-1'), data={'email': user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        email_values = mock_send.mock_calls[0]
        reset_url = email_values[-1]['reset_url']
        token = urlparse(reset_url).path.split('/')[-2]

        response = self.client.post(
            reverse('public-user-forgot-password-step-2'),
            data={'token': token, 'user_id': user.id, 'password': new_password},
            format='json'
        )
        user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(new_password))

    @patch('apps.mail.models.Mail.send')
    def test_user_can_request_password_icase(self, mock_send):
        create_email = 'USER@example.com'
        reset_email = 'user@EXAMPLE.com'
        get_user_model().objects.create_user(
            email=create_email,
            password='secret',)
        response = self.client.post(
            reverse('public-user-forgot-password-step-1'), data={'email': reset_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
