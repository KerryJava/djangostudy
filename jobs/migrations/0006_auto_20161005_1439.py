# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-05 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20161005_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='color_code',
            field=models.CharField(default=0, max_length=6),
        ),
        migrations.AddField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
