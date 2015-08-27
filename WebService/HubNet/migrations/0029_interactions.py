# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0028_auto_20150617_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeStamp', models.DateTimeField(null=True, verbose_name=b'time stamp')),
                ('tagId1', models.CharField(max_length=255)),
                ('tagId2', models.CharField(max_length=255)),
                ('event', models.ForeignKey(to='HubNet.Event', null=True)),
                ('sensor', models.ForeignKey(to='HubNet.Sensor', null=True)),
            ],
            options={
                'ordering': ('timeStamp',),
            },
        ),
    ]
