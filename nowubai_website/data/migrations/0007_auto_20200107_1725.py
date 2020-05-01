# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-07 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_teacher_teacher_tutor_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=30, unique=True, verbose_name='课程名称'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade_name',
            field=models.CharField(max_length=20, unique=True, verbose_name='年级名称'),
        ),
    ]