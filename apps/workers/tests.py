from datetime import timedelta
from unittest.mock import patch
from django.db.models import Q
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.workers.tasks import test
from apps.workers.models import Task

string = "something to print"
future_time = timezone.now() + timedelta(minutes=10)


class WorkerTests(APITestCase):
    @patch('apps.user.mail.Mail.send')
    def test_sample_task_creation(self, mock_send):
        """
        Ensure we can queue a sample task.
        """
        old_task_ids = Task.objects.all().values_list('id', flat=True)
        old_task_count = Task.objects.all().count()
        test(string)
        new_task = Task.objects.filter(Q(id__in=old_task_ids)).first()
        new_task_count = Task.objects.all().count()
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task_count - old_task_count, 1)
        self.assertEqual(new_task.args, f'["{string}"]')

    def test_task_direct_run(self):
        """
        Ensure we can run a sample task directly.
        """
        string = "something to print"
        testing_direct_run = test(string, now=True)
        self.assertEqual(testing_direct_run, string)

    def test_task_schedule_time(self):
        """
        Ensure we can run a sample task at specific time.
        """
        old_task_ids = Task.objects.all().values_list('id', flat=True)
        old_task_count = Task.objects.all().count()
        test(string, _schedule=future_time)
        new_task = Task.objects.filter(Q(id__in=old_task_ids)).first()
        new_task_count = Task.objects.all().count()
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task_count - old_task_count, 1)
        self.assertEqual(new_task.args, f'["{string}"]')
        self.assertEqual(new_task.run_at, future_time)
