# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-06 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_remove_image_fk_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.ImageField(upload_to='', verbose_name='图片路径'),
        ),
    ]
