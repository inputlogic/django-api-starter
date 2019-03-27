from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Layout


class LayoutTests(TestCase):
    def test_body_validation(self):
        self.assertRaises(
            ValidationError,
            Layout.objects.create,
            name='Bodyless Layout',
            html='<html>Welcome</html>'
        )
