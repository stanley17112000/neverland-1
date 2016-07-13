# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_neverland', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_id', models.IntegerField(verbose_name='relation_id')),
                ('uid1', models.IntegerField(verbose_name='uid1')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='fb_id',
            field=models.CharField(max_length=100, verbose_name='fb_id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='last_name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='local',
            field=models.CharField(max_length=100, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick_name',
            field=models.CharField(max_length=100, verbose_name='nick_name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(max_length=100, verbose_name='profile_pic'),
        ),
    ]