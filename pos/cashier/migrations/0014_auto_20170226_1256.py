# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-26 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0013_product_promotion_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='member',
            name='addr',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='member',
            name='ic',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='member',
            name='member_id',
            field=models.CharField(default=10001, max_length=20),
        ),
        migrations.AddField(
            model_name='member',
            name='tel',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]