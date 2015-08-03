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
            name='userProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True)),
                ('nid', models.CharField(max_length=10, null=True, verbose_name='National Identity', blank=True)),
                ('insurance', models.CharField(max_length=10, null=True, verbose_name='Sport`s Insurance Number', blank=True)),
                ('cellPhone', models.CharField(help_text='example: 09121231234', max_length=11, null=True, verbose_name='Cell Phone', blank=True)),
                ('landline', models.CharField(help_text='With area code - example: 02122334455', max_length=12, null=True, verbose_name='Landline', blank=True)),
                ('postalcode', models.CharField(max_length=10, null=True, verbose_name='Postal Code', blank=True)),
                ('address', models.CharField(max_length=400, null=True, verbose_name='Address', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('profile_is_update', 'Profile updated'), ('club_owner', 'Club owner')),
            },
        ),
    ]
