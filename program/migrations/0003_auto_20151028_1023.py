# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_auto_20150811_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programdefinition',
            name='created',
            field=models.DateTimeField(verbose_name='created', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='programdefinition',
            name='genderLimit',
            field=models.IntegerField(default=1, help_text='Please select gender if there is limitation', verbose_name='Gender', choices=[(1, 'Male/Female'), (2, 'Male'), (3, 'Female'), (4, 'Seperate')]),
        ),
        migrations.AlterField(
            model_name='programdefinition',
            name='status',
            field=models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')]),
        ),
        migrations.AlterField(
            model_name='programdefinition',
            name='updated',
            field=models.DateTimeField(verbose_name='updated', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='programdefinition',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
