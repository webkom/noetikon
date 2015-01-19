from django.test import TestCase
from rest_framework.reverse import reverse


class LoginRequiredTestCase(TestCase):

    def assertLoginRequired(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('?next={}'.format(url) in response.url)

    def test_directory_list(self):
        self.assertLoginRequired(reverse('directory-list'))

    def test_directory_detail(self):
        self.assertLoginRequired(reverse('directory-detail', args=['slug']))

    def test_file_detail(self):
        self.assertLoginRequired(reverse('file-detail', args=['slug']))

    def test_file_download(self):
        self.assertLoginRequired(reverse('file-download', args=['slug']))
