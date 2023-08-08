from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APITestCase


class UserChangePasswordTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-change-password')
        self.user = mixer.blend(get_user_model())
        self.user.set_password('oldpassword')
        self.user.save()
        self.new_password = 'newPassword1'

    def test_user_change_password_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {'password': 'oldpassword',
                                     'new_password': self.new_password},
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_change_password_unauthenticated(self):
        response = self.client.post(self.url,
                                    {'password': self.user.password,
                                     'new_password': self.new_password},
                                    format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_change_password_incorrect_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {'password': 'incorrectPassword',
                                     'new_password': self.new_password},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0],
                         'Invalid current password.')

    def test_user_change_password_same(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {'password': 'oldpassword',
                                     'new_password': 'oldpassword'},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        error_detail = response.data.get('non_field_errors')
        error_message = error_detail[0]
        self.assertEqual(
            error_message,
            'New password should be different from the current password.')

    def test_user_change_password_too_common(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url,
                                    {'password': 'oldpassword',
                                     'new_password': 'newpassword'},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        error_detail = response.data.get('non_field_errors')
        error_message = error_detail[0]
        self.assertEqual(error_message,
                         'This password is too common.')
