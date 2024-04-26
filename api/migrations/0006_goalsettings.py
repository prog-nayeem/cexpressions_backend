# Generated by Django 5.0.4 on 2024-04-26 17:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_understandinggoalprioritization_is_active_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_to_achive', models.CharField()),
                ('purpose_of_goal', models.CharField()),
                ('plan_to_implement', models.CharField()),
                ('area_of_focus', models.CharField()),
                ('target_completion_date', models.DateField()),
                ('priority_scale', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=20)),
                ('goal_term', models.CharField(choices=[('short_term', 'Short Term'), ('long_term', 'Long Term')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
