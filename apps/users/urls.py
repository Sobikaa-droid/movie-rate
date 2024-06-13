from django.contrib import admin
from django.urls import include, path, re_path

app_name = 'users'

urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]