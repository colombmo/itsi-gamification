# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0010_auto_20141119_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesttag',
            name='description',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
