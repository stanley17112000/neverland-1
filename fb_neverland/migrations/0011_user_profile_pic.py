# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_neverland', '0010_auto_20160713_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='', max_length=100, verbose_name='profile_pic'),
        ),
    ]
