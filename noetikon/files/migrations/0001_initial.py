# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import basis.models
from django.conf import settings
from django.db import migrations, models

import noetikon.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('deleted', models.BooleanField(editable=False, default=False)),
                ('path', models.TextField(unique=True)),
                ('slug', models.TextField(unique=True, editable=False)),
                ('groups_with_access', models.ManyToManyField(to='auth.Group', null=True, blank=True)),
                ('parent_folder', models.ForeignKey(to='files.Directory', related_name='children', blank=True, null=True)),
                ('users_with_access', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'directories',
                'ordering': ['path'],
            },
            bases=(noetikon.files.models.FilePropertyMixin, models.Model),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False, default=basis.models._now)),
                ('updated_at', models.DateTimeField(editable=False, default=basis.models._now)),
                ('deleted', models.BooleanField(editable=False, default=False)),
                ('path', models.TextField(unique=True)),
                ('slug', models.TextField(unique=True, editable=False)),
                ('created_by', models.ForeignKey(editable=False, related_name='file_created', to=settings.AUTH_USER_MODEL, default=None, null=True)),
                ('parent_folder', models.ForeignKey(to='files.Directory')),
                ('updated_by', models.ForeignKey(editable=False, related_name='file_updated', to=settings.AUTH_USER_MODEL, default=None, null=True)),
            ],
            options={
                'ordering': ['path'],
            },
            bases=(noetikon.files.models.FilePropertyMixin, models.Model),
        ),
    ]
