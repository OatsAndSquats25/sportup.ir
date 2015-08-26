# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0003_auto_20150813_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolledprogram',
            name='firstAccess',
            field=models.BooleanField(default=False),
        ),
    ]
