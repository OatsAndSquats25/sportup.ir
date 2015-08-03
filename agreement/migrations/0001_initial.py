# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('context', models.TextField()),
                ('commission', models.DecimalField(default=0.05, verbose_name='Commission percentage', max_digits=4, decimal_places=3)),
                ('agreementStatus', models.IntegerField(default=3, verbose_name='Agreement status', choices=[(1, 'Draft'), (2, 'Request'), (3, 'Processing'), (4, 'Active'), (5, 'Pending'), (6, 'Canceled'), (7, 'Expired')])),
                ('finBank', models.CharField(max_length=100, verbose_name='Customer bank name')),
                ('finBranch', models.CharField(max_length=100, verbose_name='Customer bank branch')),
                ('finAccount', models.CharField(max_length=100, verbose_name='Customer bank account number')),
                ('finOwner', models.CharField(max_length=100, verbose_name='Customer bank account owner')),
                ('finDescription', models.CharField(max_length=100, null=True, verbose_name='Description', blank=True)),
                ('clubKey', models.ForeignKey(to='directory.club')),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Agreement',
            },
        ),
    ]
