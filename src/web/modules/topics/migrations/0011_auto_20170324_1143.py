# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0010_filltopicsquestionnaireentrancestep_text_questionnaire_is_on_checking_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicquestionnaire',
            name='previous',
            field=models.ForeignKey(blank=True, help_text='Её оценки используются для автоматического заполнения этой ТА', null=True, on_delete=django.db.models.deletion.CASCADE, to='topics.TopicQuestionnaire'),
        ),
        migrations.AlterField(
            model_name='topiccheckingquestionnairequestion',
            name='checker_result',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'OK'), (2, 'WRONG ANSWER'), (3, 'PRESENTATION ERROR'), (4, 'CHECK FAILED')], default=None, null=True, validators=[djchoices.choices.ChoicesValidator({1: 'OK', 2: 'WRONG ANSWER', 3: 'PRESENTATION ERROR', 4: 'CHECK FAILED'})]),
        ),
    ]
