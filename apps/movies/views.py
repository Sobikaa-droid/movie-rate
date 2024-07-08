from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.views import generic
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
import requests

from .models import Movie
from .permissions import IsStaffUser, IsStaffUserOrReadOnly
from .serializers import MovieSerializer, MovieCreateSerializer, MovieCreateListSerializer


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
                    response = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f').json()
                else:
                    response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey=9a6fa81f').json()

                error = response.get('Error')
                if error:
                    return Response(
                        {'error': error},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                obj, created = Movie.objects.get_or_create(
                        title=response.get('Title', 'N/A'),
                        year=response.get('Year', 'N/A'),
                        defaults={
                            'genre': response.get('Genre', 'N/A').split(", "),
                            'rating': float(response.get('imdbRating', 0)) if response.get('imdbRating') != 'N/A' else float(0),
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
                    response = requests.get(f'https://www.omdbapi.com/?t={slugify(title)}&apikey=9a6fa81f').json()

                    obj, created = Movie.objects.get_or_create(
                        title=response.get('Title', 'N/A'),
                        year=response.get('Year', 'N/A'),
                        defaults={
                            'genre': response.get('Genre', 'N/A').split(", "),
                            'rating': float(response.get('imdbRating', 0)) if response.get('imdbRating') != 'N/A' else float(0),
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
                response = requests.get(f'https://www.omdbapi.com/?t={slugify(movie.title)}&year={slugify(movie.year)}&apikey=9a6fa81f').json()
                
                movie.title=response.get('Title', 'N/A')
                movie.year=response.get('Year', 'N/A')
                movie.genre=response.get('Genre', 'N/A').split(", ")
                movie.rating=float(response.get('imdbRating', 0)) if response.get('imdbRating') != 'N/A' else float(0)
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
    paginate_by = 10
    template_name = "movies/movie_list.html"

    def get_queryset(self):
        qs = super().get_queryset().all()

        filter_val = self.request.GET.get('filter_val', None)
        search_val = self.request.GET.get('search_val', None)
        order_val = self.request.GET.get('order_by', None)
        if filter_val:
            qs = qs.filter(type__icontains=filter_val)
        if search_val:
            qs = qs.filter(title__icontains=search_val)
        if order_val:
            qs = qs.order_by(order_val)

        return qs


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.exclude(pk=self.kwargs.get('pk')).all().order_by('?')
        response = requests.get(f'https://www.omdbapi.com/?t={slugify(self.object.title)}&year={slugify(self.object.year)}&apikey=9a6fa81f').json()
        context['imdb_votes'] = response.get('imdbVotes', 'N/A')
        context['imdb_rating'] = float(response.get('imdbRating', '0'))

        return context
