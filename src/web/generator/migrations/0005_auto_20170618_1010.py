# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-18 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20170212_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abstractdocumentblock',
            options={'ordering': ('document', 'order'), 'verbose_name': 'document block'},
        ),
        migrations.AlterModelOptions(
            name='abstracttablestylecommand',
            options={'verbose_name': 'table style command'},
        ),
        migrations.AlterField(
            model_name='linetablestylecommand',
            name='command_name',
            field=models.CharField(choices=[('LINEAFTER', 'Lineafter'), ('LINEBEFORE', 'Linebefore'), ('BOX', 'Box'), ('GRID', 'Grid'), ('INNERGRID', 'Innergrid'), ('LINEBELOW', 'Linebelow'), ('LINEABOVE', 'Lineabove'), ('OUTLINE', 'Outline')], max_length=100),
        ),
    ]
