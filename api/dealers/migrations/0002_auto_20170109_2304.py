# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-09 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dealerscraper',
            options={'ordering': ['class_name']},
        ),
    ]
