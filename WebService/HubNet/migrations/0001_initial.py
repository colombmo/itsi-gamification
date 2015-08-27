# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('startdate', models.DateTimeField(verbose_name='start date')),
                ('stopdate', models.DateTimeField(verbose_name='stop date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterestTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=7)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tagId', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1)),
                ('interestTags', models.ForeignKey(to='HubNet.InterestTag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tagId', models.CharField(max_length=255)),
                ('rssi', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('identifier', models.IntegerField(unique=True)),
                ('description', models.CharField(max_length=200)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('radius', models.FloatField()),
                ('records', models.ForeignKey(to='HubNet.Record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='interestTags',
            field=models.ForeignKey(to='HubNet.InterestTag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ForeignKey(to='HubNet.Participant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='sensors',
            field=models.ForeignKey(to='HubNet.Sensor'),
            preserve_default=True,
        ),
    ]
