# Generated by Django 2.0.3 on 2018-05-10 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dates', '0005_auto_20180510_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkeydateexception',
            name='key_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_exceptions', to='dates.KeyDate'),
        ),
    ]
