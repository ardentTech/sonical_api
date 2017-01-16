# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-16 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_auto_20170116_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='bl_product',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='BL Product (Tm)'),
        ),
        migrations.AddField(
            model_name='driver',
            name='diaphragm_mass_including_airload',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Diaphragm Mass Inc. Airload (g)'),
        ),
    ]
