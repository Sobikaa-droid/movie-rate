from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
