# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='created',
            field=models.DateTimeField(verbose_name='created', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='access',
            name='status',
            field=models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')]),
        ),
        migrations.AlterField(
            model_name='access',
            name='updated',
            field=models.DateTimeField(verbose_name='updated', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='access',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
