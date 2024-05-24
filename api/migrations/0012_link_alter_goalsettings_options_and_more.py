# Generated by Django 5.0.4 on 2024-05-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_goalsettings_goal_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=500)),
            ],
        ),
        migrations.AlterModelOptions(
            name='goalsettings',
            options={'verbose_name': 'Goal Setting', 'verbose_name_plural': 'Goal Settings'},
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'verbose_name': 'Progress', 'verbose_name_plural': 'Progresses'},
        ),
        migrations.AlterModelOptions(
            name='suggestionsforsuccess',
            options={'verbose_name': 'Suggestion for Success', 'verbose_name_plural': 'Suggestions for Success'},
        ),
    ]
