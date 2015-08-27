# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0016_auto_20141120_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='gender',
        ),
    ]
