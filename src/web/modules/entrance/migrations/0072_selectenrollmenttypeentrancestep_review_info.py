# Generated by Django 2.0.3 on 2018-04-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0071_auto_20180409_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectenrollmenttypeentrancestep',
            name='review_info',
            field=models.TextField(blank=True, default='', help_text='Поддерживается Markdown', verbose_name='информация для модераторов'),
        ),
    ]
