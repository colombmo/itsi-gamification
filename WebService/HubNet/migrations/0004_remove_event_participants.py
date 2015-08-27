# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0003_auto_20141118_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
    ]
