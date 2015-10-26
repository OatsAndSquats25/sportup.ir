# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0002_auto_20151026_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='userCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('originValue', models.IntegerField(default=0, verbose_name='Origin Credit')),
                ('value', models.IntegerField(default=0, verbose_name='Credit')),
                ('invoiceKey', models.ForeignKey(blank=True, to='finance.invoice', null=True)),
                ('user', models.ForeignKey(default=1, verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
