# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Images', '0002_excelfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfiles',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
