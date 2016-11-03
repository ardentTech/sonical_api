# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 04:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manufacturing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diameter', models.FloatField(blank=True, null=True, verbose_name='Diameter (Millimeters)')),
                ('max_power', models.IntegerField(blank=True, null=True, verbose_name='Max Power (Watts)')),
                ('model', models.CharField(blank=True, max_length=128, verbose_name='Model')),
                ('nominal_impedance', models.IntegerField(blank=True, null=True, verbose_name='Nominal Impedance (Ohms)')),
                ('resonant_frequency', models.FloatField(blank=True, null=True, verbose_name='Resonant Frequency (Hertz)')),
                ('rms_power', models.IntegerField(blank=True, null=True, verbose_name='RMS power (Watts)')),
                ('sensitivity', models.FloatField(blank=True, null=True, verbose_name='Sensitivity (Decibels)')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturing.Manufacturer')),
            ],
            options={
                'ordering': ['model'],
            },
        ),
    ]
