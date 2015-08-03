# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('summary', models.TextField(max_length=200, verbose_name='Summary')),
                ('detail', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('website', models.CharField(max_length=100, verbose_name='Website')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('cell', models.CharField(max_length=20, verbose_name='Cell')),
                ('logo', models.ImageField(upload_to=b'', verbose_name='Logo')),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='imageCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('imageFile', models.ImageField(upload_to=b'', verbose_name='File')),
                ('clubKey', models.ForeignKey(related_query_name=b'imageCollection', related_name='imageCollection', to='directory.club')),
            ],
        ),
    ]
