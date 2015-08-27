# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0025_auto_20150529_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='reference',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='tagId',
            field=models.CharField(max_length=255),
        ),
    ]
