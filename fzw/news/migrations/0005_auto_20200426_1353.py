# pylint: disable=invalid-name
# Generated by Django 3.0.4 on 2020-04-26 13:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20180325_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
