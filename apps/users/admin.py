from django.contrib import admin
from .models import TunedUser


class TunedUserAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(TunedUser, TunedUserAdmin)
