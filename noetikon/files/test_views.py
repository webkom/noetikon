from django.test import TestCase
from rest_framework.reverse import reverse
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
