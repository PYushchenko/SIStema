# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-21 21:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sistema.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionnaire', '0003_auto_20170515_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionnaireTypingDynamics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typing_data', sistema.models.CompressedTextField(help_text='JSON с данными о нажатиях клавиш')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='should_record_typing_dynamics',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questionnairetypingdynamics',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='questionnaire.Questionnaire'),
        ),
        migrations.AddField(
            model_name='questionnairetypingdynamics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]