from django.contrib.auth.models import AbstractUser


class TunedUser(AbstractUser):
    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
