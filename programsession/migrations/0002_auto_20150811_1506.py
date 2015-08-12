# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programsession', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionrestriction',
            name='capacityDiff',
            field=models.IntegerField(null=True, verbose_name='Capacity Increase/Decrease', blank=True),
        ),
    ]
