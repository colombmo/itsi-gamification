# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0002_auto_20141118_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='records',
            field=models.ForeignKey(blank=True, to='HubNet.Record'),
            preserve_default=True,
        ),
    ]
