from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import default_storage
import os

from apps.movies.models import MovieReview, FavMovie, MovieRating, MovieWatchLater


class Country(models.Model):
    common_name = models.CharField(max_length=150)
    cca2 = models.CharField(max_length=30)

    class Meta:
        ordering = ['common_name']

    def __str__(self):
        return f'{self.common_name} [{self.cca2}]'


def delete_file(instance, field):
    field_value = getattr(instance, field, None)

    # Check if the field value is not None and the file exists
    if field_value and default_storage.exists(field_value.path):
        default_storage.delete(field_value.path)


def get_upload_path(instance, filename):
    first_letter = instance.username[0].capitalize()
    if first_letter not in list('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        first_letter = '$'
    folder_path = f"users/{first_letter}/"
    return os.path.join(folder_path, filename)


class TunedUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    second_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    year_of_birth = models.DateField(null=True, blank=True)
    country = models.OneToOneField(Country, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        # Delete the old image if a new one is being uploaded
        if self.pk:
            old_instance = TunedUser.objects.get(pk=self.pk)
            if self.image != old_instance.image:
                delete_file(old_instance, 'image')
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
    