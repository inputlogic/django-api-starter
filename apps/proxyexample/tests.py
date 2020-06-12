import unittest

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProxyTests(APITestCase):
    @unittest.skip("proxy tests are prone to fail")
    def set_token(self, email, password):
        url = reverse('login')
        response = self.client.post(
            url,
            data={'email': email, 'password': password},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    @unittest.skip("proxy tests are prone to fail")
    def test_proxy(self):
        get_user_model().objects.create_user(
            email='user1@example.com',
            password='secret1'
        )
        url = reverse('proxy-user-list')

        payload = {
            "company": "test",
            "filter": "foo"
        }

        response = self.client.post(url, data={**payload}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.set_token('user1@example.com', 'secret1')
        response = self.client.post(url, data={**payload}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
