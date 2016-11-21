# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-18 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0010_paymentrecord_table_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_from', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('remark', models.TextField(blank=True)),
                ('orders', models.CharField(blank=True, max_length=100)),
                ('card_no', models.IntegerField(blank=True, default=0, max_length=8, null=True)),
                ('table_no', models.IntegerField(blank=True, default=0, max_length=8, null=True)),
                ('per_hrs', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('pay_status', models.CharField(default='0', max_length=5)),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Member')),
            ],
        ),
    ]
