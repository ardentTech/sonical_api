# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0001_initial'),
        ('drivers', '0004_auto_20170117_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='cone_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_cone_material', to='manufacturing.Material', verbose_name='cone material'),
        ),
        migrations.AddField(
            model_name='driver',
            name='surround_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_surround_material', to='manufacturing.Material', verbose_name='surround material'),
        ),
    ]