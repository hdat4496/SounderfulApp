# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounderful', '0003_auto_20171123_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
