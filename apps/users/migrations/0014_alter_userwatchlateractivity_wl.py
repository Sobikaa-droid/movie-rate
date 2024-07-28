# Generated by Django 5.0.6 on 2024-07-24 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_moviewatchlater_and_more'),
        ('users', '0013_userwatchlateractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwatchlateractivity',
            name='wl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wl_activity_set', to='movies.moviewatchlater'),
        ),
    ]