# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0008_auto_20141119_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='interesttag',
            options={'ordering': ('description',)},
        ),
        migrations.AlterField(
            model_name='interesttag',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, to='HubNet.Event'),
            preserve_default=True,
        ),
    ]
