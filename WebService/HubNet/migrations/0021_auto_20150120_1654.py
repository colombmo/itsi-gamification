# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0020_auto_20150120_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='markers',
        ),
        migrations.AddField(
            model_name='marker',
            name='event',
            field=models.ForeignKey(default=3, to='HubNet.Event'),
            preserve_default=False,
        ),
    ]
