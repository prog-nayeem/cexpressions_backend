# Generated by Django 5.0.4 on 2024-04-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'required': 'Please provide your email address.', 'unique': 'A user with this email address already exists.'}, max_length=255, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(error_messages={'required': 'Please provide your full name.'}, max_length=100, verbose_name='Full Name'),
        ),
    ]
