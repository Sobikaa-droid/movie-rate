from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserFavoriteActivity, UserReviewActivity, UserRatingActivity, UserWatchLaterActivity
from apps.movies.models import MovieRating, MovieReview, FavMovie, MovieWatchLater


# REVIEW
@receiver(post_save, sender=MovieReview)
def log_review_activity(sender, instance, created, **kwargs):
    UserReviewActivity.objects.create(
        user=instance.user,
        review=instance,
        type='review',
    )


@receiver(post_delete, sender=MovieReview)
def log_review_delete_activity(sender, instance, **kwargs):
    qs = UserReviewActivity.objects.filter(user=instance.user, review=instance)
    if qs.exists():
        qs.first().delete()


# RATING
@receiver(post_save, sender=MovieRating)
def log_rating_activity(sender, instance, created, **kwargs):
    """ qs = UserActivity.objects.filter(user=instance.user, content_object=instance)
    if qs.exists():
        qs.first().delete() """

    UserRatingActivity.objects.create(
        user=instance.user,
        rating=instance,
        type='rating',
    )


@receiver(post_delete, sender=MovieRating)
def log_rating_delete_activity(sender, instance, **kwargs):
    qs = UserRatingActivity.objects.filter(user=instance.user, rating=instance)
    if qs.exists():
        qs.first().delete()


# FAVORITE 
@receiver(post_save, sender=FavMovie)
def log_favorite_activity(sender, instance, created, **kwargs):
    UserFavoriteActivity.objects.create(
        user=instance.user,
        favorite=instance,
        type='favorite',
    )


@receiver(post_delete, sender=FavMovie)
def log_favorite_delete_activity(sender, instance, **kwargs):
    qs = UserFavoriteActivity.objects.filter(user=instance.user, favorite=instance)
    if qs.exists():
        qs.first().delete()


# WATCH LATER
@receiver(post_save, sender=MovieWatchLater)
def log_wl_activity(sender, instance, created, **kwargs):
    UserWatchLaterActivity.objects.create(
        user=instance.user,
        wl=instance,
        type='wl',
    )


@receiver(post_delete, sender=MovieWatchLater)
def log_wl_delete_activity(sender, instance, **kwargs):
    qs = UserWatchLaterActivity.objects.filter(user=instance.user, wl=instance)
    if qs.exists():
        qs.first().delete()