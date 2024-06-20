from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'movies'

urlpatterns = [
    # api
    path('api/create/<slug:title>/', views.CreateMovieAPIView.as_view(), name='api_create_movie'),
    path('api/create-list/<int:limit>/', views.CreateMovieListAPIView.as_view(), name='api_create_movie_list'),
    path('api/list/', views.MovieAPIListView.as_view(), name='api_movie_list'),
    path('api/detail/<int:pk>/', views.MovieAPIRetrieveDestroyView.as_view(), name='api_movie_retrievedestroy'),
    # generic
]
