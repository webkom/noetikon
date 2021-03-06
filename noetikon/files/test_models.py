import os
import shutil
from datetime import datetime
from io import StringIO
from unittest import mock

from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.test import TestCase
from PIL import Image

from noetikon.files.models import Directory, File


class BaseTestCase(TestCase):

    def setUp(self):
        self.path = os.path.join(settings.MEDIA_ROOT, 'test')
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(os.path.join(self.path, 'subdir'), exist_ok=True)
        self.test_file = os.path.join(os.path.dirname(settings.BASE_DIR), 'requirements.txt')
        shutil.copyfile(
            self.test_file,
            os.path.join(self.path, 'requirements.txt')
        )
        self.directory = Directory.objects.create(path=self.path)
        self.directory.update_content(verbose=False)

    def tearDown(self):
        shutil.rmtree(self.path)


class DirectoryTestCase(BaseTestCase):

    def test_str(self):
        self.assertEqual(str(self.directory), self.directory.name)

        with mock.patch('noetikon.files.models.Directory.name', None):
            self.assertEqual(str(Directory()), '')

    def test_exists(self):
        self.assertTrue(self.directory.exists)

        directory = Directory.objects.create(path=self.path + 'n')
        self.assertFalse(directory.exists)
        directory.delete()

    def test_name(self):
        self.assertEqual(self.directory.name, 'test')

    def test_size(self):
        self.assertGreater(self.directory.size, 0)

    def test_parents(self):
        self.assertEqual(len(self.directory.children.last().parents), 1)
        self.assertEqual(self.directory.children.last().parents[0].pk, self.directory.pk)

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
                self.test_file,
                os.path.join(self.path, 'r.txt')
            )
            self.directory.update_content(verbose=True)
            self.assertTrue('test/r.txt\n' in fake_out.getvalue())
            self.assertTrue('..' in fake_out.getvalue())


class FileTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.file_path = os.path.join(self.path, 'requirements.txt')
        self.file = File.objects.get(path=self.file_path)
        self.non_existing_file = File.objects.create(
            path=self.path + 'n',
            parent_folder=self.directory
        )

    def test_str(self):
        self.assertEqual(str(self.file), self.file.name)

        with mock.patch('noetikon.files.models.File.name', None):
            self.assertEqual(str(File()), '')

    def test_exists(self):
        self.assertTrue(self.file.exists)
        self.assertFalse(self.non_existing_file.exists)

    def test_name(self):
        self.assertEqual(self.file.name, 'requirements.txt')

    def test_size(self):
        self.assertEqual(self.file.size, 25)
        self.assertEqual(filesizeformat(self.file.size), '25\xa0bytes')
        self.assertEqual(self.non_existing_file.size, 0)

    def test_modified_time(self):
        today = datetime.today()
        self.assertAlmostEqual(self.file.modified_time.year, today.year)
        self.assertAlmostEqual(self.file.modified_time.month, today.month)
        self.assertAlmostEqual(self.file.modified_time.day, today.day)

    def test_slug(self):
        self.assertEqual(self.file.slug, 'test/requirements.txt')

    def test_content(self):
        self.assertEqual(self.file.content, '-r requirements/base.txt\n')

    def test_thumbnail(self):
        image_path = os.path.join(self.directory.path, 'test_logo.jpg')
        image = Image.new('L', (500, 500))
        image.save(image_path)
        file = File.objects.create(parent_folder=self.directory, path=image_path)
        thumbnail = file.thumbnail()
        self.assertIsNotNone(thumbnail)
        os.remove(image_path)
        file.delete(force=True)

    def test_extension(self):
        self.assertEqual(self.file.extension, 'txt')
        file = File(path='file.PNG')
        self.assertEqual(file.extension, 'png')
        file = File(path='file...PNG')
        self.file.save()
        self.assertEqual(file.extension, 'png')

    def test_rendered_content(self):
        with mock.patch('pypandoc.convert') as mock_pypandoc:
            self.file.rendered_content()
            self.assertTrue(mock_pypandoc.called)
        self.assertEqual(self.file.rendered_content(), self.file.content)

    def test_is_image(self):
        with mock.patch('noetikon.files.models.File.extension', 'png'):
            self.assertTrue(self.file.is_image())
        with mock.patch('noetikon.files.models.File.extension', 'txt'):
            self.assertFalse(self.file.is_image())

    def test_fa_icon(self):
        with mock.patch('noetikon.files.models.File.extension', 'png'):
            self.assertTrue(self.file.fa_icon(), 'image-o')

        with mock.patch('noetikon.files.models.File.extension', 'zip'):
            self.assertTrue(self.file.fa_icon(), 'archive-o')

        with mock.patch('noetikon.files.models.File.extension', 'docx'):
            self.assertTrue(self.file.fa_icon(), 'word-o')

        with mock.patch('noetikon.files.models.File.extension', 'xlsx'):
            self.assertTrue(self.file.fa_icon(), 'excel-o')

        with mock.patch('noetikon.files.models.File.extension', 'ppt'):
            self.assertTrue(self.file.fa_icon(), 'powerpoint-o')

        with mock.patch('noetikon.files.models.File.extension', 'pdf'):
            self.assertTrue(self.file.fa_icon(), 'pdf-o')

        with mock.patch('noetikon.files.models.File.extension', 'txt'):
            self.assertTrue(self.file.fa_icon(), 'text-o')

        with mock.patch('noetikon.files.models.File.extension', 't'):
            self.assertTrue(self.file.fa_icon(), 'file-o')

    def test_x_redirect_url(self):
        self.assertEqual(self.file.x_redirect_url, '/protected/test/requirements.txt')

    def test_ignore_files(self):
        shutil.copyfile(
            self.test_file,
            os.path.join(self.path, '.DS_Store')
        )
        self.directory.update_content(verbose=False)
        self.assertEqual(self.directory.files.all().count(), 2)
