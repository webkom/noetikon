from io import StringIO
import os
import shutil
from datetime import datetime
from unittest import mock
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.test import TestCase

from noetikon.files.models import Directory, File


class BaseTestCase(TestCase):

    def setUp(self):
        self.path = os.path.join(settings.MEDIA_ROOT, 'test')
        os.makedirs(self.path)
        os.mkdir(os.path.join(self.path, 'subdir'))
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), '../../../noetikon/requirements.txt'),
            os.path.join(self.path, 'requirements.txt')
        )
        self.directory = Directory.objects.create(path=self.path)
        self.directory.update_content(verbose=False)

    def tearDown(self):
        shutil.rmtree(self.path)


class DirectoryTestCase(BaseTestCase):

    def test_str(self):
        self.assertEqual(str(self.directory), self.directory.name)

    def test_exists(self):
        self.assertTrue(self.directory.exists)

        directory = Directory.objects.create(path=self.path + 'n')
        self.assertFalse(directory.exists)
        directory.delete()

    def test_name(self):
        self.assertEqual(self.directory.name, 'test')

    def test_size(self):
        self.assertEqual(self.directory.size, 229)
        self.assertEqual(filesizeformat(self.directory.size), '229\xa0bytes')

    def test_modified_time(self):
        today = datetime.today()
        self.assertAlmostEqual(self.directory.modified_time.year, today.year)
        self.assertAlmostEqual(self.directory.modified_time.month, today.month)
        self.assertAlmostEqual(self.directory.modified_time.day, today.day)

    def test_slug(self):
        self.assertEqual(self.directory.slug, 'test')
        self.assertEqual(self.directory.children.last().slug, 'test/subdir')

    def test_update_content_delete(self):
        directory = Directory.objects.create(path=os.path.join(self.path, 'n'))
        directory.update_content()
        self.assertEqual(Directory.objects.filter(path=directory.path).count(), 0)
        self.assertEqual(Directory.all_objects.filter(path=directory.path).count(), 1)

    def test_update_content_output(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), '../../../noetikon/requirements.txt'),
                os.path.join(self.path, 'r.txt')
            )
            self.directory.update_content(verbose=True)
            self.assertEqual(fake_out.getvalue(), '/Users/rolf/backup/test/r.txt\n..')


class FileTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.file_path = os.path.join(self.path, 'requirements.txt')
        self.file = File.objects.get(path=self.file_path)

    def test_str(self):
        self.assertEqual(str(self.directory), self.directory.name)

    def test_exists(self):
        self.assertTrue(self.file.exists)

        file_object = File.objects.create(path=self.path + 'n', parent_folder=self.directory)
        self.assertFalse(file_object.exists)
        file_object.delete()

    def test_name(self):
        self.assertEqual(self.file.name, 'requirements.txt')

    def test_size(self):
        self.assertEqual(self.file.size, 25)
        self.assertEqual(filesizeformat(self.file.size), '25\xa0bytes')

    def test_modified_time(self):
        today = datetime.today()
        self.assertAlmostEqual(self.file.modified_time.year, today.year)
        self.assertAlmostEqual(self.file.modified_time.month, today.month)
        self.assertAlmostEqual(self.file.modified_time.day, today.day)

    def test_slug(self):
        self.assertEqual(self.file.slug, 'test/requirementstxt')

    def test_extension(self):
        self.assertEqual(self.file.extension, 'txt')
        file = File(path='file.PNG')
        self.assertEqual(file.extension, 'png')
        file = File(path='file...PNG')
        self.file.save()
        self.assertEqual(file.extension, 'png')

    def test_is_image(self):
        with mock.patch('noetikon.files.models.File.extension', 'png'):
            self.assertTrue(self.file.is_image())
        with mock.patch('noetikon.files.models.File.extension', 'txt'):
            self.assertFalse(self.file.is_image())

    def test_x_redirect_url(self):
        self.assertEqual(self.file.x_redirect_url, '/protected/test/requirements.txt')
