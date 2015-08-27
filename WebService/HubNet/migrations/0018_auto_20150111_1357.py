# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0017_remove_participant_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='sex',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensor',
            name='rssiThreshold',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
