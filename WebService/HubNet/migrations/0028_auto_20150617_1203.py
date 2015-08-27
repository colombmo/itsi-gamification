# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0027_auto_20150530_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='rssi',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='radius',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='rssiThreshold',
        ),
        migrations.AlterField(
            model_name='participant',
            name='tagId',
            field=models.CharField(max_length=255),
        ),
    ]
