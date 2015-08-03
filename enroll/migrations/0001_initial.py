# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='enrolledProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=12, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Enroll',
                'verbose_name_plural': 'Enroll',
            },
        ),
        migrations.CreateModel(
            name='enrolledProgramCourse',
            fields=[
                ('enrolledprogram_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='enroll.enrolledProgram')),
                ('firstTime', models.BooleanField(default=True, verbose_name='First time remaining flag')),
            ],
            options={
                'abstract': False,
            },
            bases=('enroll.enrolledprogram',),
        ),
        migrations.AddField(
            model_name='enrolledprogram',
            name='invoiceKey',
            field=models.ForeignKey(blank=True, to='finance.invoice', null=True),
        ),
        migrations.AddField(
            model_name='enrolledprogram',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_enroll.enrolledprogram_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='enrolledprogram',
            name='programDefinitionKey',
            field=models.ForeignKey(to='program.programDefinition'),
        ),
        migrations.AddField(
            model_name='enrolledprogram',
            name='user',
            field=models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
