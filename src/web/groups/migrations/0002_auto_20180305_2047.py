# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-05 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractgroup',
            name='name',
            field=models.CharField(help_text='Покороче, используется на метках', max_length=60),
        ),
    ]
