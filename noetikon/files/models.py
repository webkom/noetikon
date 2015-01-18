import os

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from basis.models import PersistentModel, BasisModel
import sys
from sorl.thumbnail.shortcuts import get_thumbnail

from noetikon.helpers import slugify
from .managers import DirectoryManager, FileManager


class FilePropertyMixin(object):
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


class Directory(FilePropertyMixin, PersistentModel):
    path = models.TextField(unique=True)
    slug = models.TextField(unique=True, editable=False)
    parent_folder = models.ForeignKey('self', related_name='children', null=True, blank=True)
    users_with_access = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)
    groups_with_access = models.ManyToManyField('auth.Group', null=True, blank=True)

    objects = DirectoryManager()

    class Meta:
        verbose_name_plural = 'directories'
        ordering = ['path']

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.parent_folder is not None:
            self.slug = os.path.join(self.parent_folder.slug, slugify(os.path.basename(self.path)))
        else:
            self.slug = slugify(os.path.basename(self.path))
        super().save(*args, **kwargs)

    def update_content(self, verbose=True):
        if not os.path.exists(self.path):
            self.delete()
            return False

        for item in os.listdir(self.path):
            created = False
            path = os.path.join(self.path, item)
            if os.path.isdir(path):
                directory, created = Directory.objects.get_or_create(path=path, parent_folder=self)
                directory.users_with_access = self.users_with_access.all()
                directory.groups_with_access = self.groups_with_access.all()
                directory.update_content(verbose)
            elif os.path.isfile(path):
                created = File.objects.get_or_create(path=path, parent_folder=self)[1]

            if verbose:
                if created:
                    print(path)
                else:
                    sys.stdout.write('.')


class File(FilePropertyMixin, BasisModel):
    path = models.TextField(unique=True)
    slug = models.TextField(unique=True, editable=False)
    parent_folder = models.ForeignKey(Directory, related_name='files')

    objects = FileManager()

    class Meta:
        ordering = ['path']

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        self.slug = os.path.join(self.parent_folder.slug, slugify(os.path.basename(self.path)))
        super().save(*args, **kwargs)

    def is_image(self):
        return os.path.splitext(self.path) in settings.FILE_TYPES['image']

    @property
    def x_redirect_url(self):
        return '/protected{}'.format(self.path.replace(settings.STORAGE_BASE_PATH, ''))
