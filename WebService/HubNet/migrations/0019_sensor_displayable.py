# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0018_auto_20150111_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='displayable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
