from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.user.factories import UserFactory
from .models import File


class FileTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email='test@example.org')
        self.client.force_authenticate(user=self.user)

    def test_upload_file(self):
        url = reverse('upload-file',)
        file_data = SimpleUploadedFile("file.jpg", b"this is image", content_type="image/jpeg")
        response = self.client.post(url, {'upload': file_data})
        self.assertTrue(response.data['is_verified'])
        self.assertIn('url', response.data)

    def test_signed_file(self):
        url = reverse('create-signed-file',)
        response = self.client.post(url, {'file_name': "file.jpg"}, format='json')
        self.assertIn('file_id', response.data)
        self.assertIn('url', response.data)
        self.assertIn('s3_data', response.data)
        self.assertIn('url', response.data['s3_data'])
        self.assertIn('fields', response.data['s3_data'])
        self.assertEqual(response.data['url'], File.objects.last().upload.url)
