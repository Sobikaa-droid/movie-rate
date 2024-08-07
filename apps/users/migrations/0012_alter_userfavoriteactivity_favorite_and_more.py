# Generated by Django 5.0.6 on 2024-07-23 02:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_remove_moviereview_unique_review_movie_per_user'),
        ('users', '0011_userfavoriteactivity_userratingactivity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavoriteactivity',
            name='favorite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_activity_set', to='movies.favmovie'),
        ),
        migrations.AlterField(
            model_name='userratingactivity',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_activity_set', to='movies.movierating'),
        ),
    ]
