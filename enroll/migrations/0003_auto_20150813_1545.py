# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0002_enrolledprogramsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolledprogramsession',
            name='date',
            field=models.DateField(verbose_name='Specific date'),
        ),
        migrations.AlterField(
            model_name='enrolledprogramsession',
            name='sessionTimeBegin',
            field=models.TimeField(verbose_name='Begin time'),
        ),
        migrations.AlterField(
            model_name='enrolledprogramsession',
            name='sessionTimeEnd',
            field=models.TimeField(verbose_name='End time'),
        ),
    ]
