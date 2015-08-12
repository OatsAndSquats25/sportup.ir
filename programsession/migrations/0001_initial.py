# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='sessionDefinition',
            fields=[
                ('programdefinition_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='program.programDefinition')),
                ('sessionTimeBegin', models.TimeField(null=True, verbose_name='Begin time', blank=True)),
                ('sessionTimeEnd', models.TimeField(null=True, verbose_name='End time', blank=True)),
                ('sessionDuration', models.TimeField(verbose_name='Session duration')),
                ('daySat', models.BooleanField(verbose_name='Saturday')),
                ('daySun', models.BooleanField(verbose_name='Sunday')),
                ('dayMon', models.BooleanField(verbose_name='Monday')),
                ('dayTue', models.BooleanField(verbose_name='Tuesday')),
                ('dayWed', models.BooleanField(verbose_name='Wedensday')),
                ('dayThu', models.BooleanField(verbose_name='Thursday')),
                ('dayFri', models.BooleanField(verbose_name='Friday')),
                ('daysToShow', models.IntegerField(default=7, verbose_name='Numberof weeks to show')),
            ],
            options={
                'abstract': False,
            },
            bases=('program.programdefinition',),
        ),
        migrations.CreateModel(
            name='sessionRestriction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, verbose_name='Specific date', blank=True)),
                ('day', models.IntegerField(null=True, verbose_name='Day of week', blank=True)),
                ('sessionTimeBegin', models.TimeField(null=True, verbose_name='Begin time', blank=True)),
                ('sessionTimeEnd', models.TimeField(null=True, verbose_name='End time', blank=True)),
                ('capacityDiff', models.IntegerField(verbose_name='Capacity Increase/Decrease')),
                ('blackout', models.BooleanField(verbose_name='Blockout')),
                ('sessionDefinitionKey', models.ForeignKey(to='programsession.sessionDefinition')),
            ],
        ),
    ]
