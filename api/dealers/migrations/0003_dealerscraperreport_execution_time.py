# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-27 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0002_auto_20170119_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealerscraperreport',
            name='execution_time',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Execution Time'),
            preserve_default=False,
        ),
    ]