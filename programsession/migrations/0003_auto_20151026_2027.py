# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programsession', '0002_auto_20150811_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessiondefinition',
            options={'verbose_name': 'Definition', 'verbose_name_plural': 'Definitions'},
        ),
        migrations.AlterModelOptions(
            name='sessionrestriction',
            options={'verbose_name': 'Restriction', 'verbose_name_plural': 'Restrictions'},
        ),
        migrations.AlterField(
            model_name='sessiondefinition',
            name='dayWed',
            field=models.BooleanField(verbose_name='Wednesday'),
        ),
        migrations.AlterField(
            model_name='sessiondefinition',
            name='daysToShow',
            field=models.IntegerField(default=7, verbose_name='Number of next days to show'),
        ),
    ]
