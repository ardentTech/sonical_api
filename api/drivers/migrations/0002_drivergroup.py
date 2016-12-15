# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('drivers', models.ManyToManyField(blank=True, to='drivers.Driver', verbose_name='drivers')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]