# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='enrolledProgramSession',
            fields=[
                ('enrolledprogram_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='enroll.enrolledProgram')),
                ('date', models.DateField(null=True, verbose_name='Specific date', blank=True)),
                ('sessionTimeBegin', models.TimeField(null=True, verbose_name='Begin time', blank=True)),
                ('sessionTimeEnd', models.TimeField(null=True, verbose_name='End time', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('enroll.enrolledprogram',),
        ),
    ]
