import os

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse

from noetikon.files.models import File
from noetikon.files.test_models import BaseTestCase
from noetikon.helpers.test_mixins import LoginRequiredTestMixin


class LoginRequiredTestCase(LoginRequiredTestMixin, TestCase):

    def test_directory_list(self):
        self.assertLoginRequired(reverse('directory-list'))

    def test_directory_detail(self):
        self.assertLoginRequired(reverse('directory-detail', args=['slug']))

    def test_file_detail(self):
        self.assertLoginRequired(reverse('file-detail', args=['slug']))

    def test_file_download(self):
        self.assertLoginRequired(reverse('file-download', args=['slug']))


class SmokeTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.file_path = os.path.join(self.path, 'requirements.txt')
        self.file = File.objects.get(path=self.file_path)
        credentials = {'username': 'dumbledore', 'password': 'acid pops'}
        self.user = User.objects.create_superuser(email='boss@da.com', **credentials)
        self.client.login(**credentials)

    def test_directory_list(self):
        response = self.client.get(reverse('directory-list'))
        self.assertContains(response, self.directory.name)

    def test_directory_detail(self):
        response = self.client.get(reverse('directory-detail', args=[self.directory.slug]))
        self.assertContains(response, self.directory.name)
        self.assertContains(response, self.file.name)

    def test_file_detail(self):
        response = self.client.get(reverse('file-detail', args=[self.file.slug]))
        self.assertContains(response, self.file.name)

    def test_file_download(self):
        response = self.client.get(reverse('file-download', args=[self.file.slug]))
        self.assertEqual(response['X-Accel-Redirect'], '/protected/test/requirements.txt')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="requirements.txt"')
