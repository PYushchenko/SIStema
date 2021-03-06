# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poldnev', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('last_name', 'first_name', 'middle_name')},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('-poldnev_id',)},
        ),
        migrations.AddField(
            model_name='session',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
