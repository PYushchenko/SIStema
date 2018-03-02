# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20170515_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='has_accepted_terms',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
    ]
