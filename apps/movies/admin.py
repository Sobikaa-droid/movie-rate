from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(Movie, MovieAdmin)
