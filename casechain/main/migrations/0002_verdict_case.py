# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verdict',
            name='case',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Case'),
            preserve_default=False,
        ),
    ]
