# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0031_auto_20150629_1002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interaction',
            options={'ordering': ('event', 'count')},
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='timeStamp',
        ),
        migrations.AddField(
            model_name='interaction',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
