# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-03 08:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=datetime.datetime(2016, 11, 3, 8, 0, 43, 775371, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='end_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='start_from',
            field=models.DateTimeField(auto_now=True),
        ),
    ]