# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0026_auto_20150529_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='tagId',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
