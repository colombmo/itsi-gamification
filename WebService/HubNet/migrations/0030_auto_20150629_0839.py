# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0029_interactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
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
        migrations.RemoveField(
            model_name='interactions',
            name='event',
        ),
        migrations.RemoveField(
            model_name='interactions',
            name='sensor',
        ),
        migrations.DeleteModel(
            name='Interactions',
        ),
    ]
