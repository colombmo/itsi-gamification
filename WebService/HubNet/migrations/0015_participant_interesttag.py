# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0014_auto_20141119_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='interestTag',
            field=models.ForeignKey(null=True, blank=True, to='HubNet.InterestTag'),
            preserve_default=True,
        ),
    ]
