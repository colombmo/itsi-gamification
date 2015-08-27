# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0009_auto_20141119_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interesttag',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='interestTags',
            field=models.ManyToManyField(null=True, to='HubNet.InterestTag', blank=True),
            preserve_default=True,
        ),
    ]
