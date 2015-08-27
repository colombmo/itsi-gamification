# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0023_auto_20150122_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='firstName',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='lastName',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
