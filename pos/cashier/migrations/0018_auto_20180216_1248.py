# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-02-16 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0017_auto_20180216_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrecord',
            name='price_type',
            field=models.CharField(default='1', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='price_type',
            field=models.CharField(default='1', max_length=5, null=True),
        ),
    ]
