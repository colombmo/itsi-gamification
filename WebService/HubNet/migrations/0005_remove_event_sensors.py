# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0004_remove_event_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sensors',
        ),
    ]
