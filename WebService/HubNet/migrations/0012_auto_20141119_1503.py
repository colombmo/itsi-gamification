# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0011_auto_20141119_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ('tagId',)},
        ),
        migrations.RemoveField(
            model_name='participant',
            name='interestTags',
        ),
        migrations.AddField(
            model_name='event',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, to='HubNet.Participant'),
            preserve_default=True,
        ),
    ]
