# Generated by Django 2.0.3 on 2018-05-10 20:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dates', '0004_3_unique_school_and_short_name_20180323_2115'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KeyDateException',
            new_name='UserKeyDateException',
        ),
    ]
