from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import requests


class Movie(models.Model):
    title = models.CharField(max_length=350)
    year = models.IntegerField()
    genre = models.JSONField()
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    director = models.CharField(max_length=150)
    actors = models.JSONField()
    plot = models.TextField(max_length=9999)
    poster = models.URLField()
    runtime = models.IntegerField()
    country = models.CharField(max_length=100)
    production = models.CharField(max_length=200)


    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.title} ({self.year})'
    
    def get_absolute_url(self):
        return reverse('movies:detail', args=[self.pk])
    
"""     def save(self, *args, **kwargs):
        title = slugify(str(self.title))
        year = int(self.year)
        response = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f')
        self.poster = response.json().get('Poster')

        super().save(*args, **kwargs) """

