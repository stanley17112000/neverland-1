# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_neverland', '0002_auto_20160713_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_Pic',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('uid', models.CharField(max_length=100, verbose_name='uid')),
                ('url', models.CharField(max_length=100, verbose_name='url')),
            ],
        ),
        migrations.RemoveField(
            model_name='relation',
            name='relation_id',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='uid1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fb_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='user',
            name='current_relation_id',
            field=models.IntegerField(default=-1, verbose_name='current_relation_id'),
        ),
        migrations.AddField(
            model_name='user',
            name='flag',
            field=models.BooleanField(default=False, verbose_name='flag'),
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default='', max_length=100, verbose_name='uid'),
        ),
    ]