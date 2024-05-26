# Generated by Django 5.0.4 on 2024-05-24 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_link_alter_goalsettings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='is_share_app',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='link',
            name='share_app_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]