# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-12 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0005_paymentrecord_pay_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrecord',
            name='pay_status',
            field=models.CharField(default='0', max_length=5),
        ),
    ]
