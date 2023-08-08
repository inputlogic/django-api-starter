from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APITestCase


class UserChangeEmailTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-change-email')
        self.user = mixer.blend(get_user_model())
        self.user.set_password('onepass')
        self.user.save()
        self.new_email = 'newemail@gmail.com'

    def test_user_change_email_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {
                                        'password': 'onepass',
                                        'new_email': self.new_email
                                    },
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_change_email_unauthenticated(self):
        response = self.client.post(self.url,
                                    {
                                        'password': 'onepass',
                                        'new_email': self.new_email
                                    },
                                    format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_change_email_incorrect_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {
                                        'password': 'incorrectPassword',
                                        'new_email': self.new_email
                                    },
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0],
                         'Invalid password.')
