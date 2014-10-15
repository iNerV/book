# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(max_length=200, upload_to='/', null=True)),
                ('gender', models.CharField(max_length=6, blank=True, null=True)),
                ('birth_date', models.CharField(max_length=200, blank=True, null=True)),
                ('site', models.URLField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('num_series', models.PositiveIntegerField()),
                ('ru_desc', models.TextField(null=True)),
                ('en_desc', models.TextField(null=True)),
                ('other_desc', models.TextField(null=True)),
                ('book_cover', models.ImageField(max_length=200, upload_to='/')),
                ('isbn10', models.PositiveIntegerField(max_length=10, null=True)),
                ('isbn13', models.PositiveIntegerField(max_length=13, null=True)),
                ('asin', models.CharField(max_length=10, null=True)),
                ('url', models.PositiveIntegerField()),
                ('author', models.ManyToManyField(to='books.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gr_id', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gr_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ManyToManyField(to='books.Series', null=True),
            preserve_default=True,
        ),
    ]
