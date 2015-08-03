# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='courseDays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dayOfWeek', models.CharField(max_length=3, verbose_name='Day of week', choices=[(b'SAT', 'Saturday'), (b'SUN', 'Sunday'), (b'MON', 'Monday'), (b'TUE', 'Tuesday'), (b'WED', 'Wednesday'), (b'THU', 'Thursday'), (b'FRI', 'Friday')])),
                ('dateOfDay', models.DateField(null=True, verbose_name='Date of day', blank=True)),
                ('sessionTimeBegin', models.TimeField(null=True, verbose_name='Begin time', blank=True)),
                ('sessionTimeEnd', models.TimeField(null=True, verbose_name='End time', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='courseDefinition',
            fields=[
                ('programdefinition_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='program.programDefinition')),
                ('usageBeginChoices', models.IntegerField(default=1, help_text='Usage begin policy since enroll', verbose_name='Usage can begin from', choices=[(1, 'Enrollment'), (2, 'First login'), (3, 'Specific date')])),
                ('usageBeginDate', models.DateField(help_text='Set this field if usage will start at specific date', null=True, verbose_name='Begin date of usage', blank=True)),
                ('usageEndDate', models.DateField(help_text='Set this field if usage will finish at specific date', null=True, verbose_name='End date of usage', blank=True)),
                ('maxDays', models.IntegerField(help_text='Maximum valid days since enroll choice', null=True, verbose_name='Maximum valid day', blank=True)),
                ('maxSessions', models.IntegerField(help_text='Maximum sessions', null=True, verbose_name='Maximum allowed session', blank=True)),
                ('expireDate', models.DateField(null=True, verbose_name='Membership expire date', blank=True)),
            ],
            options={
                'verbose_name': 'Course definition',
                'verbose_name_plural': 'Courses definition',
            },
            bases=('program.programdefinition',),
        ),
        migrations.AddField(
            model_name='coursedays',
            name='courseDefinitionKey',
            field=models.ForeignKey(to='programcourse.courseDefinition'),
        ),
    ]
