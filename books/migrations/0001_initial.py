# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ASIN',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('asin', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(max_length=200, upload_to='/', null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('birth_date', models.CharField(blank=True, max_length=200, null=True)),
                ('site', models.URLField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('ru_desc', models.TextField(null=True)),
                ('en_desc', models.TextField(null=True)),
                ('other_desc', models.TextField(null=True)),
                ('book_cover', models.ImageField(max_length=200, upload_to='/')),
                ('num_series', models.PositiveIntegerField(blank=True, null=True)),
                ('gr_id', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrId',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('gr_id', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ISBN10',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('isbn10', models.PositiveIntegerField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ISBN13',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('isbn13', models.PositiveIntegerField(max_length=13)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('gr_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='book',
            name='all_titles',
            field=models.ForeignKey(blank=True, null=True, to='books.Titles'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='asin',
            field=models.ManyToManyField(blank=True, null=True, to='books.ASIN'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(to='books.Author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='isbn10',
            field=models.ManyToManyField(blank=True, null=True, to='books.ISBN10'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='isbn13',
            field=models.ManyToManyField(blank=True, null=True, to='books.ISBN13'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ManyToManyField(blank=True, null=True, to='books.Series'),
            preserve_default=True,
        ),
    ]
