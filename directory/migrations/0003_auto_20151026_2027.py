# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0002_auto_20150908_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='locationKey',
            field=models.ForeignKey(related_query_name=b'club', related_name='complexLocation', verbose_name='Location', blank=True, to='directory.complexLocation', null=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complexlocation',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complextitle',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='genre',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
