# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('file_path', models.CharField(max_length=128, validators=[utils.validators.validate_file_path], verbose_name='file path')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ScraperReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('attempted', models.PositiveIntegerField(default=0, verbose_name='attempted')),
                ('processed', models.PositiveIntegerField(default=0, verbose_name='processed')),
                ('scraper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapers.Scraper', verbose_name='scraper')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
