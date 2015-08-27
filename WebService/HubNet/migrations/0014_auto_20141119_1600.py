# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0013_auto_20141119_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ('tagId',)},
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='records',
        ),
        migrations.AddField(
            model_name='event',
            name='sensors',
            field=models.ManyToManyField(to='HubNet.Sensor', blank=True, null=True),
            preserve_default=True,
        ),
    ]
