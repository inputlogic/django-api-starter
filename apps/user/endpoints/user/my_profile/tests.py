from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APITestCase


class UserMyProfileTests(APITestCase):
    def setUp(self):
        self.user = mixer.blend(get_user_model())
        self.url = reverse('user-my-profile')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_authenticated(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 401)
