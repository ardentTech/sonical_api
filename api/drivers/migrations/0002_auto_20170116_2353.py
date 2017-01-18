# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-16 23:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manufacturing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivergroup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='drivergroup',
            name='drivers',
            field=models.ManyToManyField(blank=True, to='drivers.Driver', verbose_name='drivers'),
        ),
        migrations.AddField(
            model_name='driver',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturing.Manufacturer'),
        ),
    ]