from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=350)
    year = models.CharField(max_length=25)
    genre = models.JSONField()
    director = models.CharField(max_length=150)
    actors = models.JSONField()
    plot = models.TextField(max_length=9999)
    poster = models.URLField()
    runtime = models.CharField(max_length=25)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    total_seasons = models.CharField(blank=True, null=True, max_length=30)
    slug = models.SlugField(blank=True, null=True, max_length=350)


    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.title} ({self.year})'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title))

        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('movies:detail', args=[self.slug, self.pk])
    

"""     def save(self, *args, **kwargs):
        title = slugify(str(self.title))
        year = int(self.year)
        response = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f')
        self.poster = response.json().get('Poster')

        super().save(*args, **kwargs) """


class FavMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='fav_movie_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fav_user_set')

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_fav_movie_per_user')
        ]

    def __str__(self):
        return f"{self.user}: {self.movie}"
    

class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rating_movie_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rating_user_set')
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(1)])
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_rating_movie_per_user')
        ]

    def __str__(self):
        return f"{self.user}: {self.movie} - {self.rating}"


class MovieReview(models.Model):
    title = models.CharField(max_length=50)
    memo = models.TextField(max_length=2000)
    impression = models.IntegerField(default=0, validators=[MaxValueValidator(1), MinValueValidator(-1)])
    creation_date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review_movie_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_user_set')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f"{self.user}: {self.movie} - {self.impression}"
    

class MovieWatchLater(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='wl_movie_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wl_user_set')

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_wl_movie_per_user')
        ]

    def __str__(self):
        return f"{self.user}: {self.movie}"
    