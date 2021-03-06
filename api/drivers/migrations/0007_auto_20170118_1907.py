# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0001_initial'),
        ('drivers', '0006_auto_20170118_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='basket_frame',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_basket_frame', to='manufacturing.Material', verbose_name='basket frame'),
        ),
        migrations.AddField(
            model_name='driver',
            name='magnet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_magnet', to='manufacturing.Material', verbose_name='magnet'),
        ),
    ]
