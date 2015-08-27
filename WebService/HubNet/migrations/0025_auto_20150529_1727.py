# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0024_auto_20150521_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ('reference',)},
        ),
        migrations.AlterField(
            model_name='participant',
            name='reference',
            field=models.IntegerField(default=1, unique=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participant',
            name='tagId',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
