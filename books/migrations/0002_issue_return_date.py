# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-27 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]