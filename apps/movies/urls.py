from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'movies'

urlpatterns = [
    # api
    path('api/movies/', views.MovieAPIListView.as_view(), name='api_movie_list'),
    path('api/movies/create/', views.CreateMovieListAPIView.as_view(), name='api_create_movie_list'),
    path('api/movies/update/', views.UpdateMovieListAPIView.as_view(), name='api_update_movie_list'),
    path('api/movie/<int:pk>/', views.MovieAPIRetrieveDestroyView.as_view(), name='api_movie_retrievedestroy'),
    path('api/movie/create/', views.CreateMovieAPIView.as_view(), name='api_create_movie'),

    path('api/ratings/<int:movie_pk>/', views.MovieRatingAPIListCreateView.as_view(), name='api_rating_lc'),
    path('api/rating/<int:pk>/', views.MovieRatingAPIRetrieveDestroyView.as_view(), name='api_rating_rd'),
    path('api/favorites/<int:movie_pk>/', views.MovieFavoriteAPIListCreateView.as_view(), name='api_favorite_lc'),
    path('api/favorite/<int:pk>/', views.MovieFavoriteAPIDestroyView.as_view(), name='api_favorite_d'),
    path('api/reviews/<int:movie_pk>/', views.MovieReviewAPIListCreateView.as_view(), name='api_review_lc'),
    path('api/review/<int:pk>/', views.MovieReviewAPIRetrieveUpdateDestroyView.as_view(), name='api_review_rud'),
    path('api/wls/<int:movie_pk>/', views.MovieWatchLaterAPIListCreateView.as_view(), name='api_wl_lc'),
    path('api/wl/<int:pk>/', views.MovieWatchLaterAPIDestroyView.as_view(), name='api_wl_d'),
    # generic
    path('', views.MovieListView.as_view(), name='list'),
    path('detail/<slug:slug>-<int:pk>/', views.MovieDetailView.as_view(), name='detail'),

    path('fav-movie/<int:pk>/', login_required(views.fav_or_unfav_movie, login_url='users:register'), name='fav_movie'),
    path('wl-movie/<int:pk>/', login_required(views.wl_or_unwl_movie, login_url='users:register'), name='wl_movie'),
    path('rate-movie/<int:pk>/', login_required(views.rate_movie, login_url='users:register'), name='rate_movie'),
    path('delete-rating/<int:pk>/', login_required(views.MovieRatingDeleteView.as_view(), login_url='users:register'), name='delete_rating'),
    path('reviews/<slug:slug>-<int:pk>/', login_required(views.MovieReviewListView.as_view(), login_url='users:register'), name='review_list'),
    path('review-movie/<int:pk>/', login_required(views.review_movie, login_url='users:register'), name='review_movie'),
    path('update-review/<int:pk>/', login_required(views.MovieReviewUpdateView.as_view(), login_url='users:register'), name='update_review'),
    path('delete-review/<int:pk>/', login_required(views.MovieReviewDeleteView.as_view(), login_url='users:register'), name='delete_review'),
]
