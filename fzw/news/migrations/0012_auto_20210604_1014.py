# pylint: disable=invalid-name
# Generated by Django 3.2.3 on 2021-06-04 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_news_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='creation_time',
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2018, 2, 18, 0, 0),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='modification_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
