from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from . import mail


def stub_forgot_password_email(calls):
    def forgot_password_email(user, reset_token):
        calls.append((reset_token, user.id))
    return forgot_password_email


class UserTests(APITestCase):
    def test_register_user(self):
        """
        Ensure we can register a new user object.
        """
        url = reverse('signup')
        data = {'email': 'test@example.org', 'password': 'yayhooray'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('userId', response.data)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, 'test@example.org')

    def test_login_user(self):
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',)
        url = reverse('login')
        data = {'email': 'user@example.com', 'password': 'secret'}
        response = self.client.post(url, data, format='json')
        self.assertIn('token', response.data)
        self.assertIn('userId', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_profile(self):
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('me'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_reset_password(self):
        new_password = 'whatever'
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',)
        email_values = []
        mail.MailResetPassword.send = stub_forgot_password_email(email_values)
        response = self.client.post(
            reverse('forgot-password'), data={'email': user.email}, format='json')
        self.assertEqual(len(email_values), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        (token, user_id) = email_values[0]
        response = self.client.post(
            reverse('reset-password'),
            data={'token': token, 'user_id': user_id, 'password': new_password},
            format='json'
        )
        user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(new_password))
