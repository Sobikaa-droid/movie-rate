# Generated by Django 5.0.6 on 2024-06-28 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_total_seasons_movie_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(max_length=25),
        ),
    ]
