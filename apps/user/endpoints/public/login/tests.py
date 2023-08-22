from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from mixer.backend.django import mixer
from rest_framework.test import APITestCase


class PublicLoginTests(APITestCase):
    def setUp(self):
        self.url = reverse('public-user-login')
        self.user = mixer.blend(get_user_model())
        self.user.set_password('onepass')
        self.user.save()

    def test_public_login(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url,
                                    {
                                        'password': 'onepass',
                                        'email': self.user.email
                                    },
                                    format='json')
        self.assertEqual(response.status_code, 200)

    def test_public_login_icase(self):
        create_email = 'USER@example.com'
        login_email = 'user@EXAMPLE.com'
        get_user_model().objects.create_user(
            email=create_email,
            password='secret',)
        data = {'email': login_email, 'password': 'secret'}
        response = self.client.post(self.url, data, format='json')
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_login_incorrect_password(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url,
                                    {
                                        'password': 'incorrectPassword',
                                        'email': self.user.email
                                    },
                                    format='json')
        self.assertEqual(response.status_code, 400)
