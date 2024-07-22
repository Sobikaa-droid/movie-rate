from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserActivity
from apps.movies.models import MovieRating, MovieReview, FavMovie


# REVIEW
@receiver(post_save, sender=MovieReview)
def log_review_activity(sender, instance, created, **kwargs):
    UserActivity.objects.create(
        user=instance.user,
        active_review=instance,
        type='review',
    )


@receiver(post_delete, sender=MovieReview)
def log_review_delete_activity(sender, instance, **kwargs):
    qs = UserActivity.objects.filter(user=instance.user, active_review=instance)
    if qs.exists():
        qs.first().delete()


# RATING
@receiver(post_save, sender=MovieRating)
def log_rating_activity(sender, instance, created, **kwargs):
    """ qs = UserActivity.objects.filter(user=instance.user, content_object=instance)
    if qs.exists():
        qs.first().delete() """

    UserActivity.objects.create(
        user=instance.user,
        active_rating=instance,
        type='rating',
    )


@receiver(post_delete, sender=MovieRating)
def log_rating_delete_activity(sender, instance, **kwargs):
    qs = UserActivity.objects.filter(user=instance.user, active_rating=instance)
    if qs.exists():
        qs.first().delete()


# FAVORITE 
@receiver(post_save, sender=FavMovie)
def log_favorite_activity(sender, instance, created, **kwargs):
    UserActivity.objects.create(
        user=instance.user,
        active_favorite=instance,
        type='favorite',
    )


@receiver(post_delete, sender=FavMovie)
def log_favorite_delete_activity(sender, instance, **kwargs):
    qs = UserActivity.objects.filter(user=instance.user, active_favorite=instance)
    if qs.exists():
        qs.first().delete()
