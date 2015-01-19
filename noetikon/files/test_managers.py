import os
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase

from noetikon.files.models import Directory, File


def _create_path(*parts):
    return os.path.join(settings.MEDIA_ROOT, *parts)


class BaseTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='group')
        self.superuser = User.objects.create_superuser('super', 'super@duper.com', '...')
        self.user1 = User.objects.create_user('one')
        self.user2 = User.objects.create_user('two')
        self.user2.groups.add(self.group)
        self.directory1 = Directory.objects.create(path=_create_path('test'))
        self.directory1.users_with_access.add(self.user1)
        self.directory2 = Directory.objects.create(path=_create_path('test2'))
        self.directory2.groups_with_access.add(self.group)
        self.directory2.save()


class DirectoryManagerTestCase(BaseTestCase):
    def test_user_permitted(self):
        self.assertEqual(Directory.objects.permitted(self.user1).count(), 1)
        self.assertTrue(self.directory1 in Directory.objects.permitted(self.user1))

    def test_group_permitted(self):
        self.assertEqual(Directory.objects.permitted(self.user2).count(), 1)
        self.assertTrue(self.directory2 in Directory.objects.permitted(self.user2))

    def test_superuser(self):
        self.assertEqual(Directory.objects.permitted(self.superuser).count(), 2)


class FileManagerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.file1 = File.objects.create(path=_create_path('test', 'file.txt'),
                                         parent_folder=self.directory1)
        self.file2 = File.objects.create(path=_create_path('test1', 'file.txt'),
                                         parent_folder=self.directory2)

    def test_user_permitted(self):
        self.assertEqual(File.objects.permitted(self.user1).count(), 1)
        self.assertTrue(self.file1 in File.objects.permitted(self.user1))

    def test_group_permitted(self):
        self.assertEqual(File.objects.permitted(self.user2).count(), 1)
        self.assertTrue(self.file2 in File.objects.permitted(self.user2))

    def test_superuser(self):
        self.assertEqual(File.objects.permitted(self.superuser).count(), 2)
