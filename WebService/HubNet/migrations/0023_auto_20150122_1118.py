# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0022_participant_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='reference',
            field=models.IntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
