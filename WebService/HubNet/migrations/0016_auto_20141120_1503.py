# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0015_participant_interesttag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('tagId',)},
        ),
        migrations.AlterModelOptions(
            name='sensor',
            options={'ordering': ('description', 'identifier')},
        ),
        migrations.AddField(
            model_name='record',
            name='event',
            field=models.ForeignKey(null=True, to='HubNet.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='sensor',
            field=models.ForeignKey(null=True, to='HubNet.Sensor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='timeStamp',
            field=models.DateTimeField(verbose_name='time stamp', null=True),
            preserve_default=True,
        ),
    ]
