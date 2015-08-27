# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0032_auto_20150714_1011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interaction',
            options={'ordering': ('event', 'sensor')},
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='count',
        ),
    ]
