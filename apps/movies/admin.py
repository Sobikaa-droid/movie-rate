from django.contrib import admin
from .models import Movie, FavMovie, MovieReview, MovieRating


class MovieAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(Movie, MovieAdmin)


class FavMovieAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(FavMovie, FavMovieAdmin)


class MovieReviewAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(MovieReview, MovieReviewAdmin)


class MovieRatingAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(MovieRating, MovieRatingAdmin)
