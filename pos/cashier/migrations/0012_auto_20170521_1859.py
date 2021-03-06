# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-21 18:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0011_orderrecord'),
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
        migrations.AddField(
            model_name='paymentrecord',
            name='member_price',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='promotion_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='payment_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.PaymentRecord'),
        ),
    ]
