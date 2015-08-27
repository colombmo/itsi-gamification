# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0033_auto_20150818_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='interestTags',
            field=models.ManyToManyField(to='HubNet.InterestTag', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(to='HubNet.Participant', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='sensors',
            field=models.ManyToManyField(to='HubNet.Sensor', blank=True),
        ),
    ]
