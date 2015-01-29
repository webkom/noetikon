# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='parent_folder',
            field=models.ForeignKey(to='files.Directory', related_name='files'),
            preserve_default=True,
        ),
    ]
