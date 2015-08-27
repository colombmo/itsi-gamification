# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0012_auto_20141119_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='events',
            new_name='participants',
        ),
    ]
