import os
import sys
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from basis.models import PersistentModel, TimeStampModel
from sorl.thumbnail.shortcuts import get_thumbnail

from noetikon.helpers import slugify
from .managers import DirectoryManager, FileManager


class FilePropertyMixin(object):

    def __str__(self):
        return self.name or ''

    @cached_property
    def name(self):
        if self.exists:
            return os.path.basename(self.path)

    @cached_property
    def size(self):
        if self.exists:
            return os.path.getsize(self.path)

    @cached_property
    def exists(self):
        return os.path.exists(self.path)

    @cached_property
    def modified_time(self):
        return datetime.fromtimestamp(os.path.getmtime(self.path))


class Directory(FilePropertyMixin, TimeStampModel, PersistentModel):
    path = models.TextField(unique=True)
    slug = models.TextField(unique=True, editable=False)
    parent_folder = models.ForeignKey('self', related_name='children', null=True, blank=True)
    users_with_access = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)
    groups_with_access = models.ManyToManyField('auth.Group', null=True, blank=True)

    objects = DirectoryManager()

    class Meta:
        verbose_name_plural = 'directories'
        ordering = ['path']

    def save(self, *args, **kwargs):
        if self.parent_folder is not None:
            self.slug = os.path.join(self.parent_folder.slug, slugify(os.path.basename(self.path)))
        else:
            self.slug = slugify(os.path.basename(self.path))
        super().save(*args, **kwargs)

    @cached_property
    def size(self):
        if self.exists:
            return sum(
                [os.path.getsize(self.path)] +
                [d.size for d in self.children.all()] +
                [f.size for f in self.files.all()]
            )

    def update_content(self, verbose=True):
        if not os.path.exists(self.path):
            self.delete()
            return False

        for item in os.listdir(self.path):
            created = None
            path = os.path.join(self.path, item)
            if os.path.isdir(path):
                directory, created = Directory.objects.get_or_create(path=path, parent_folder=self)
                directory.users_with_access = self.users_with_access.all()
                directory.groups_with_access = self.groups_with_access.all()
                directory.update_content(verbose)
            elif os.path.isfile(path):
                if not os.path.basename(path) in settings.IGNORE_FILES:
                    created = File.objects.get_or_create(path=path, parent_folder=self)[1]

            if verbose:
                if created:
                    print(path)
                else:
                    if created is not None:
                        sys.stdout.write('.')


class File(FilePropertyMixin, TimeStampModel, PersistentModel):
    path = models.TextField(unique=True)
    slug = models.TextField(unique=True, editable=False)
    parent_folder = models.ForeignKey(Directory, related_name='files')

    objects = FileManager()

    class Meta:
        ordering = ['path']

    def save(self, *args, **kwargs):
        self.slug = os.path.join(self.parent_folder.slug, slugify(os.path.basename(self.path)))
        super().save(*args, **kwargs)

    @cached_property
    def extension(self):
        return os.path.splitext(self.path)[1].replace('.', '').lower()

    def fa_icon(self):
        if self.is_image():
            return 'file-image-o'
        if self._is_filetype('archive'):
            return 'file-archive-o'
        if self._is_filetype('text'):
            return 'file-text-o'
        if self.extension == 'pdf':
            return 'file-pdf-o'
        if self.extension.startswith('doc'):
            return 'file-word-o'
        if self.extension.startswith('xls'):
            return 'file-excel-o'
        if self.extension.startswith('ppt'):
            return 'file-powerpoint-o'
        return 'file-o'

    def is_image(self):
        return self._is_filetype('image')

    def _is_filetype(self, file_type):
        return self.extension in settings.FILE_TYPES[file_type]

    def thumbnail(self):
        return get_thumbnail(self.path, '500')

    @property
    def x_redirect_url(self):
        return '/protected{}'.format(self.path.replace(settings.MEDIA_ROOT, ''))
