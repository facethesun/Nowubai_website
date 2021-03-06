# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-09 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_user_user_assessment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image_url', models.ImageField(upload_to='', verbose_name='学生图片路径')),
                ('fk_user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.User')),
            ],
            options={
                'db_table': 'userimage',
            },
        ),
    ]
