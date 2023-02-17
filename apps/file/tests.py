from unittest import skipIf

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from .models import File


class FileTests(APITestCase):
    def setUp(self):
        self.user = mixer.blend('user.User')
        self.client.force_authenticate(user=self.user)

    def test_upload_file(self):
        url = reverse('upload-file',)
        file_data = SimpleUploadedFile("file.jpg", b"this is image", content_type="image/jpeg")
        response = self.client.post(url, {'upload': file_data})
        self.assertTrue(response.data['is_verified'])
        self.assertIn('url', response.data)

    @skipIf(not settings.AWS_ACCESS_KEY_ID, 'Only works if S3 is configured.')
    def test_signed_file(self):
        url = reverse('create-signed-file',)
        response = self.client.post(url, {'file_name': "file.jpg"}, format='json')
        self.assertIn('file_id', response.data)
        self.assertIn('url', response.data)
        self.assertIn('s3_data', response.data)
        self.assertIn('url', response.data['s3_data'])
        self.assertIn('fields', response.data['s3_data'])
        self.assertEqual(response.data['url'], File.objects.last().upload.url)
