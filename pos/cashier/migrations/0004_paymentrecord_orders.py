# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-11 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0003_auto_20161104_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='orders',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
