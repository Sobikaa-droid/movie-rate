from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse

from apps.movies.models import MovieReview, FavMovie, MovieRating, MovieWatchLater


class TunedUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    second_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    year_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=70, null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', args=[self.pk])


class UserReviewActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_activity_user_set')
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name='review_activity_set')
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.type}'
    

class UserFavoriteActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_activity_user_set')
    favorite = models.ForeignKey(FavMovie, on_delete=models.CASCADE, related_name='favorite_activity_set')
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.type}'


class UserRatingActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rating_activity_user_set')
    rating = models.ForeignKey(MovieRating, on_delete=models.CASCADE, related_name='rating_activity_set')
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.type}'
    

class UserWatchLaterActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wl_activity_user_set')
    wl = models.ForeignKey(MovieWatchLater, on_delete=models.CASCADE, related_name='wl_activity_set')
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.type}'
    