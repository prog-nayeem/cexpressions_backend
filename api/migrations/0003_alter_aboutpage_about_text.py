# Generated by Django 5.0.4 on 2024-04-24 16:16

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_aboutpage_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='about_text',
            field=tinymce.models.HTMLField(),
        ),
    ]
