# Generated by Django 5.0.4 on 2024-05-01 06:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_goalsettings_goal_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalsettings',
            name='goal_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
