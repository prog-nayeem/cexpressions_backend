# Generated by Django 5.0.4 on 2024-05-16 20:39

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_goalsettings_goal_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalsettings',
            name='goal_date',
        ),
        migrations.RemoveField(
            model_name='goalsettings',
            name='progress_accomplishment',
        ),
        migrations.RemoveField(
            model_name='goalsettings',
            name='status',
        ),
        migrations.RemoveField(
            model_name='goalsettings',
            name='stebacks',
        ),
        migrations.RemoveField(
            model_name='goalsettings',
            name='what_will_do_next',
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_accomplishment', models.CharField(blank=True, max_length=255, null=True)),
                ('setbacks', models.CharField(blank=True, max_length=255, null=True)),
                ('what_will_do_next', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20, null=True)),
                ('goal_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='api.goalsettings')),
            ],
        ),
    ]
