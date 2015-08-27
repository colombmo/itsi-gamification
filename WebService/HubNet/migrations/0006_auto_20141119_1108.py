# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0005_remove_event_sensors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='interestTags',
        ),
        migrations.AddField(
            model_name='interesttag',
            name='event',
            field=models.ManyToManyField(to='HubNet.Event'),
            preserve_default=True,
        ),
    ]
