# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_auto_20151026_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='homepage',
            field=models.BooleanField(default=False, verbose_name='Home page selected club'),
        ),
    ]
