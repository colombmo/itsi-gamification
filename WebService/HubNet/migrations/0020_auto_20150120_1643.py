# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HubNet', '0019_sensor_displayable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200)),
                ('timeStamp', models.DateTimeField(verbose_name=b'timeStamp')),
            ],
            options={
                'ordering': ('timeStamp', 'label'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='markers',
            field=models.ForeignKey(blank=True, to='HubNet.Marker', null=True),
            preserve_default=True,
        ),
    ]
