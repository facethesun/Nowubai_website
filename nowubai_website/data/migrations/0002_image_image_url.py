# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-05 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.TextField(default='', max_length=1037139, verbose_name='图片路径'),
        ),
    ]
