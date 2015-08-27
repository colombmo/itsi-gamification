# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0006_auto_20141119_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interesttag',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='interestTags',
            field=models.ManyToManyField(to='HubNet.InterestTag'),
            preserve_default=True,
        ),
    ]
