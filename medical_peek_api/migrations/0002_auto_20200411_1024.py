# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-11 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_peek_api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileExtractor',
        ),
        migrations.RemoveField(
            model_name='medicalitem',
            name='medical_resource',
        ),
        migrations.DeleteModel(
            name='MedicalItem',
        ),
        migrations.DeleteModel(
            name='MedicalResource',
        ),
    ]