# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-12 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0006_auto_20161112_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrecord',
            name='pay_status',
            field=models.CharField(max_length=5),
        ),
    ]
