# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('address', models.TextField(max_length=300, null=True, verbose_name='Address', blank=True)),
                ('region', models.IntegerField(null=True, verbose_name='Region', blank=True)),
                ('suburb', models.CharField(max_length=50, null=True, verbose_name='Suburb', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name='City', blank=True)),
                ('postalCode', models.CharField(max_length=10, null=True, verbose_name='Postal Code', blank=True)),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, help_text='Represented as (longitude, latitude)', null=True, verbose_name='coordinate', geography=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('visit', models.IntegerField(default=0, verbose_name='Visit')),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='complexLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='complexTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('logo', models.ImageField(upload_to=b'', verbose_name='Logo')),
                ('summary', models.TextField(max_length=400, verbose_name='Summary')),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Complex',
                'verbose_name_plural': 'Complexes',
            },
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'TE', 'Tel'), (b'FA', 'Fax'), (b'TF', 'TeleFax'), (b'EM', 'Email'), (b'WB', 'Website'), (b'CE', 'CellPhone')])),
                ('content', models.CharField(default=b'none', max_length=30, verbose_name='Content')),
                ('description', models.CharField(max_length=50, null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', null=True, editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', null=True, editable=False)),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('status', models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", verbose_name='Expires on')),
                ('type', models.IntegerField(default=1, verbose_name='Type', choices=[(1, 'Behaviour'), (2, 'Traditional')])),
                ('visit', models.IntegerField(default=0, verbose_name='Visit')),
                ('categoryKeys', models.ManyToManyField(to='directory.category', verbose_name='Category')),
                ('user', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.AlterModelOptions(
            name='club',
            options={'verbose_name': 'Club', 'verbose_name_plural': 'Club'},
        ),
        migrations.AddField(
            model_name='club',
            name='coordinate',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, help_text='Represented as (longitude, latitude)', null=True, verbose_name='coordinate', geography=True),
        ),
        migrations.AddField(
            model_name='club',
            name='visit',
            field=models.IntegerField(default=0, verbose_name='Visit'),
        ),
        migrations.AlterField(
            model_name='club',
            name='created',
            field=models.DateTimeField(verbose_name='created', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='club',
            name='status',
            field=models.IntegerField(default=1, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Inactive'), (2, 'Active'), (3, 'Draft')]),
        ),
        migrations.AlterField(
            model_name='club',
            name='updated',
            field=models.DateTimeField(verbose_name='updated', null=True, editable=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='clubKey',
            field=models.ForeignKey(blank=True, to='directory.club', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='locationKey',
            field=models.ForeignKey(verbose_name='Location', blank=True, to='directory.complexLocation', null=True),
        ),
        migrations.AddField(
            model_name='complexlocation',
            name='complexKey',
            field=models.ForeignKey(verbose_name='Complex', to='directory.complexTitle'),
        ),
        migrations.AddField(
            model_name='complexlocation',
            name='user',
            field=models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='locationKey',
            field=models.ForeignKey(verbose_name='Location', to='directory.complexLocation'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='club',
            name='categoryKeys',
            field=models.ManyToManyField(to='directory.category', null=True, verbose_name='Category', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='locationKey',
            field=models.ForeignKey(verbose_name='Location', blank=True, to='directory.complexLocation', null=True),
        ),
    ]
