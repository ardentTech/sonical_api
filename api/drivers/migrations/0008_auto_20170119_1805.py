# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 18:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0007_auto_20170118_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='maximum_linear_excursion',
            new_name='max_linear_excursion',
        ),
    ]
