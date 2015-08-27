# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0007_auto_20141119_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='interestTags',
        ),
        migrations.AddField(
            model_name='interesttag',
            name='events',
            field=models.ManyToManyField(to='HubNet.Event'),
            preserve_default=True,
        ),
    ]
