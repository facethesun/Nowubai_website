# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-14 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20200113_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='user_pay_isActive',
            field=models.BooleanField(default='False', verbose_name='是否支付'),
        ),
    ]
