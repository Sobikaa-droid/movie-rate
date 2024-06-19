from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'movies'

urlpatterns = [
    # api
    path('api/create-movie-list/<int:limit>/', views.CreateMovieListAPIView.as_view(), name='create_movie_list'),
    # generic
]
