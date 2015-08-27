# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='startdate',
            new_name='startDate',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='stopdate',
            new_name='stopDate',
        ),
    ]
