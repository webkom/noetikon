# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import basis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20150118_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='file',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='directory',
            name='created_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directory',
            name='updated_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
    ]
