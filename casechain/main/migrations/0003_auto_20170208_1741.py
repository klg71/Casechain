# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 16:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_verdict_case'),
    ]

    operations = [
            migrations.RenameModel("Facts","Fact"),
            migrations.RenameModel("Views","View")
    ]