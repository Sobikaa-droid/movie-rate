# Generated by Django 5.0.6 on 2024-06-28 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.CharField(max_length=25),
        ),
    ]
