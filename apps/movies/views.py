from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.db.models import Avg, OuterRef, Q, Exists
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
import requests

from .models import Movie, FavMovie, MovieReview, MovieRating, MovieWatchLater
from .permissions import IsStaffUser, IsStaffUserOrReadOnly
from .serializers import MovieSerializer, MovieCreateSerializer, MovieCreateListSerializer
from .forms import MovieReviewForm, MovieRatingForm

# API API API

class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class MovieAPIListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = ListPagination


class MovieAPIRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsStaffUserOrReadOnly]


class CreateMovieAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        with transaction.atomic():
            serializer = MovieCreateSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.validated_data.get('title').lower()
                year = serializer.validated_data.get('year', None)
                if year:
                    response = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f')
                else:
                    response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey=9a6fa81f')

                if response.status_code != 200:
                    return Response(
                        {'error': response.status_code},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                response = response.json()
                
                obj, created = Movie.objects.get_or_create(
                        title=response.get('Title', 'N/A'),
                        year=response.get('Year', 'N/A'),
                        defaults={
                            'genre': response.get('Genre', 'N/A').split(", "),
                            'director': response.get('Director', 'N/A'),
                            'actors': response.get('Actors', 'N/A').split(", "),
                            'plot': response.get('Plot', 'N/A'),
                            'poster': response.get('Poster', 'N/A'),
                            'runtime': response.get('Runtime', 'N/A'),
                            'country': response.get('Country', 'N/A'),
                            'type': response.get('Type', 'N/A'),
                            'total_seasons': response.get('totalSeasons', 'N/A'),
                        }
                )
                if created:
                    return Response(
                        {'success': f'Successfully created {title} movie.'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': f'{title} already exists.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     


class CreateMovieListAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        with transaction.atomic():
            serializer = MovieCreateListSerializer(data=request.data)
            if serializer.is_valid():
                response_data = {}
                movies_list = [
                    'Iron Man', 'Game of Thrones', 'The Boys', 'Invincible', 'Avengers', 'Thor', 'Iron Man 2',
                    'Dune', 'Pulp Fiction', 'Avatar', 'Drive', 'Transformers', 'The Dark Knight', 'Oblivion',
                    'There Will Be Blood', 'The Hunt', 'Moneyball', 'Finding Nemo', 'Cars', 'Star Wars', 'Get Out',
                    'The Batman', 'Breaking Bad', 'True Detective', 'Pirates of the Caribbean',
                ]
                limit = int(serializer.validated_data.get('limit'))
                for title in movies_list[0:limit]:
                    response = requests.get(f'https://www.omdbapi.com/?t={slugify(title)}&apikey=9a6fa81f')

                    if response.status_code != 200:
                        return Response(
                            {'error': response.status_code},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                    response = response.json()

                    obj, created = Movie.objects.get_or_create(
                        title=response.get('Title', 'N/A'),
                        year=response.get('Year', 'N/A'),
                        defaults={
                            'genre': response.get('Genre', 'N/A').split(", "),
                            'director': response.get('Director', 'N/A'),
                            'actors': response.get('Actors', 'N/A').split(", "),
                            'plot': response.get('Plot', 'N/A'),
                            'poster': response.get('Poster', 'N/A'),
                            'runtime': response.get('Runtime', 'N/A'),
                            'country': response.get('Country', 'N/A'),
                            'type': response.get('Type', 'N/A'),
                            'total_seasons': response.get('totalSeasons', 'N/A'),
                        }
                    )
                    if created:
                        response_data.update({title: 'created'})
                    else:
                        response_data.update({title: 'exists'})

                return Response(
                    {'success': response_data},
                    status=status.HTTP_200_OK
                    )    
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMovieListAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        with transaction.atomic():
            qs = Movie.objects.all()
            for movie in qs:
                response = requests.get(f'https://www.omdbapi.com/?t={slugify(movie.title)}&year={slugify(movie.year)}&apikey=9a6fa81f')

                if response.status_code != 200:
                    return Response(
                        {'error': response.status_code},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                response = response.json()
                
                movie.title=response.get('Title', 'N/A')
                movie.year=response.get('Year', 'N/A')
                movie.genre=response.get('Genre', 'N/A').split(", ")
                movie.director=response.get('Director', 'N/A')
                movie.actors=response.get('Actors', 'N/A').split(", ")
                movie.plot=response.get('Plot', 'N/A')
                movie.poster=response.get('Poster', 'N/A')
                movie.runtime=response.get('Runtime', 'N/A')
                movie.country=response.get('Country', 'N/A')
                movie.type=response.get('Type', 'N/A')
                movie.total_seasons=response.get('totalSeasons', 'N/A')
            
                movie.save()

            return Response(
                {'success': f'Successfully updated all movies.'},
                status=status.HTTP_200_OK
            )

# GENERIC GENERIC GENERIC

class MovieListView(generic.ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 20
    template_name = "movies/movie_list.html"

    def get_queryset(self):
        qs = super().get_queryset().all().annotate(user_rating=Avg('rating_movie_set__rating'))

        filter_val = self.request.GET.get('filter_val', None)
        search_val = self.request.GET.get('search_val', None)
        genre_val = self.request.GET.get('genre_val', None)
        order_val = self.request.GET.get('order_by', '-pk')
        if filter_val:
            qs = qs.filter(type__icontains=filter_val)
        if search_val:
            qs = qs.filter(title__icontains=search_val)
        if genre_val:
            qs = qs.filter(genre__icontains=genre_val)
        qs = qs.order_by(order_val)
        if self.request.user.is_authenticated:
            qs = qs.annotate(is_saved=Exists(FavMovie.objects.filter(movie=OuterRef('pk'), user=self.request.user)))

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_genres = [
            "Action", "Adventure", "Comedy", "Drama", "Horror", "Romance", "Science Fiction", "Animation", "Documentary",
            "Crime", "Thriller", "Family", "War", "Musical", "Western", "Sports", "Mystery", "History", "Biography", "Film Noir",
            "Disaster", "Superhero", "Adult", "Experimental", "Road Movie", "Psychological", "Martial Arts", "Anthology",
            "Erotic", "Mockumentary", "Neo-Noir", "Supernatural", "Political", "Religious", "Slasher", "Surreal", "Fantasy",
            "Dystopian", "Period"
        ]
        
        context['genres'] = movie_genres

        return context


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'https://www.omdbapi.com/?t={slugify(self.object.title)}&year={slugify(self.object.year)}&apikey=9a6fa81f')
        yt_params = {
            'q': f'{self.object.title} {self.object.year} trailer',
            'type': 'video',
            'part': 'id,snippet',
            'maxResults': 1,
            'key': 'AIzaSyC1f3pjIV3DIGIglOvOIq0eMjv-8RchM_k',
        }
        yt_response = requests.get('https://www.googleapis.com/youtube/v3/search', params=yt_params)
        user = self.request.user
        reviews = MovieReview.objects.filter(movie=self.object)
        ratings = MovieRating.objects.filter(movie=self.object)
        
        context['movies'] = self.get_queryset().exclude(pk=self.kwargs.get('pk')).order_by('?')[:5]
        context['avg_site_rating'] = ratings.aggregate(Avg('rating')).get('rating__avg')
        context['votes_count'] = ratings.count()
        context['reviews_count'] = reviews.count()
        context['reviews_gte'] = reviews.select_related('user', 'movie').order_by('?')[:4]
        context['review_form'] = MovieReviewForm()
        if response.status_code == 200:
            context['imdb_votes'] = response.json().get('imdbVotes', 'N/A')
            context['imdb_rating'] = float(response.json().get('imdbRating', '0')) if response.json().get('imdbRating') != 'N/A' else float(0)
        if yt_response.status_code == 200:
            video_id = yt_response.json().get('items')[0].get('id').get('videoId')
            context['trailer'] = f'https://www.youtube.com/embed/{video_id}'
        else:
            context['trailer'] = f'https://www.youtube.com/embed/rK42auRaDDk'

            
        if user.is_authenticated:
            context['is_saved'] = self.object.fav_movie_set.filter(user=user).exists()
            context['is_wled'] = self.object.wl_movie_set.filter(user=user).exists()
            if self.object.rating_movie_set.filter(user=user).exists():
                context['my_rating'] = get_object_or_404(ratings, user=user)

        return context
    

def fav_or_unfav_movie(request, pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        faved_movie, created = FavMovie.objects.get_or_create(user=request.user, movie=movie)

        if created:
            messages.success(request, f'{movie.title} saved to favorites.')
        else:
            faved_movie.delete()
            messages.success(request, f'{movie.title} unsaved from favorites.')
    else:
        messages.error(request, f'{request.method} not allowed.')

    return redirect(request.META.get('HTTP_REFERER'))


# MOVIE RATING MOVIE RATING MOVIE RATING MOVIE RATING MOVIE RATING MOVIE RATING MOVIE RATING 


def rate_movie(request, pk):
    if request.method == 'POST':
        form = MovieRatingForm(request.POST)
        if form.is_valid():
            movie = get_object_or_404(Movie, pk=pk)
            rating = request.POST.get('rating', None)
            user = request.user

            qs = MovieRating.objects.filter(movie=movie, user=user)
            if qs.exists():
                qs.first().delete()
            MovieRating.objects.create(
                movie=movie,
                user=request.user,
                rating=rating,
            )

            messages.success(request, f'{movie.title} rated {rating}.')
        else:
            messages.error(request, form.errors)
    else:
        messages.error(request, f'{request.method} not allowed.')
    return redirect(request.META.get('HTTP_REFERER'))


""" class MovieRatingCreateView(generic.CreateView):
    form_class = MovieRatingForm

    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        user = self.request.user
        rating = MovieRating.objects.filter(movie=movie, user=user)
        if rating.exists():
            rating.delete()
        form.instance.user = user
        form.instance.movie = movie
        messages.success(self.request, f'{movie.title} rated {form.instance.rating}.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.movie.get_absolute_url() """
    

class MovieRatingDeleteView(generic.DeleteView):
    model = MovieRating

    def get_object(self, queryset=None):
        object = get_object_or_404(super().get_queryset(), user=self.request.user, pk=self.kwargs.get('pk'))

        return object

    def form_valid(self, form):
        messages.success(self.request, 'Your rating has been successfully deleted.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.object.movie.get_absolute_url()


# MOVIE REVIEW MOVIE REVIEW MOVIE REVIEW MOVIE REVIEW MOVIE REVIEW MOVIE REVIEW MOVIE REVIEW 

class MovieReviewListView(generic.ListView):
    model = MovieReview
    context_object_name = 'reviews'
    paginate_by = 10
    template_name = "movies/review_list.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related('user', 'movie').filter(movie__pk=self.kwargs.get('pk'), movie__slug=self.kwargs.get('slug'))

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        return context
    

def review_movie(request, pk):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            movie = get_object_or_404(Movie, pk=pk)
            user = request.user
            form.instance.user = user
            form.instance.movie = movie
            form.save()
            messages.success(request, f'Your review for {movie.title} has been posted.')
        else:
            messages.error(request, form.errors)
    else:
        messages.error(request, f'{request.method} not allowed.')
    return redirect(request.META.get('HTTP_REFERER'))



""" class MovieReviewCreateView(generic.CreateView):
    form_class = MovieReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        messages.success(self.request, f'{form.instance.movie} review has been posted.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.movie.get_absolute_url() """
    

class MovieReviewUpdateView(generic.UpdateView):
    model = MovieReview
    form_class = MovieReviewForm
    template_name = 'movies/review_update.html'

    def get_object(self, queryset=None):
        object = get_object_or_404(super().get_queryset(), user=self.request.user, pk=self.kwargs.get('pk'))

        return object

    def form_valid(self, form):
        messages.success(self.request, 'Your review has been updated.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.object

        return context

    def get_success_url(self):
        return reverse('movies:update_review', kwargs={'pk': self.kwargs.get('pk')})


class MovieReviewDeleteView(generic.DeleteView):
    model = MovieReview

    def get_object(self, queryset=None):
        object = get_object_or_404(super().get_queryset(), user=self.request.user, pk=self.kwargs.get('pk'))

        return object

    def form_valid(self, form):
        messages.success(self.request, 'Your Review has been successfully deleted.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.object.movie.get_absolute_url()


# WATCH LATER

def wl_or_unwl_movie(request, pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        wl_movie, created = MovieWatchLater.objects.get_or_create(user=request.user, movie=movie)

        if created:
            messages.success(request, f'{movie.title} saved to watch later.')
        else:
            wl_movie.delete()
            messages.success(request, f'{movie.title} unsaved from watch later.')
    else:
        messages.error(request, f'{request.method} not allowed.')

    return redirect(request.META.get('HTTP_REFERER'))
