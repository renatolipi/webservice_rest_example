# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('zip_code', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=150)),
                ('neighborhood', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=100)),
            ],
        ),
    ]
