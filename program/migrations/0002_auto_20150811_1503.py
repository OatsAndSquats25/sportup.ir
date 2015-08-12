# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programdefinition',
            name='brief',
            field=models.CharField(max_length=50, null=True, verbose_name='Brief', blank=True),
        ),
        migrations.AddField(
            model_name='programdefinition',
            name='description',
            field=models.TextField(null=True, verbose_name='Description about program', blank=True),
        ),
    ]
