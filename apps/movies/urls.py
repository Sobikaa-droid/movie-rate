from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'movies'

urlpatterns = [
    # api
    path('api/create/', views.CreateMovieAPIView.as_view(), name='api_create_movie'),
    path('api/create-list/', views.CreateMovieListAPIView.as_view(), name='api_create_movie_list'),
    path('api/update-list/', views.UpdateMovieListAPIView.as_view(), name='api_update_movie_list'),
    path('api/list/', views.MovieAPIListView.as_view(), name='api_movie_list'),
    path('api/detail/<int:pk>/', views.MovieAPIRetrieveDestroyView.as_view(), name='api_movie_retrievedestroy'),
    # generic
    path('', views.MovieListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.MovieDetailView.as_view(), name='detail'),
    path('fav-movie/<int:pk>/', login_required(views.fav_or_unfav_movie, login_url='users:register'), name='fav_movie'),
    path('review-movie/<int:pk>/', login_required(views.create_movie_review, login_url='users:register'), name='review_movie'),
]
