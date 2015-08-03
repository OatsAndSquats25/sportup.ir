# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('agreement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='programDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('maxCapacity', models.IntegerField(default=-1, help_text='Please fill if your program has maximum capacity', verbose_name='Maximum capacity')),
                ('remainCapacity', models.IntegerField(null=True, verbose_name='Remain capacity', blank=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=15, decimal_places=0)),
                ('ageMin', models.IntegerField(default=0, verbose_name='Age minimum')),
                ('ageMax', models.IntegerField(default=100, verbose_name='Age maximum')),
                ('genderLimit', models.IntegerField(default=1, help_text='Please select gender if there is limitation', verbose_name='Gender', choices=[(1, 'Male/Female'), (2, 'Male'), (3, 'Female')])),
                ('needInsurance', models.BooleanField(default=False, help_text='Mark if your program needs sport insurance', verbose_name='Sport insurance required')),
                ('multipleReserve', models.BooleanField(default=False, help_text='Mark if you want to permit each account can reserve multiple instance of this program', verbose_name='Multiple reserve eligibility')),
                ('agreementKey', models.ForeignKey(verbose_name='Agreement', to='agreement.agreement')),
                ('clubKey', models.ForeignKey(verbose_name='Club', to='directory.club')),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_program.programdefinition_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
