from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
import requests

from .models import Movie
from .permissions import IsStaffUser, IsStaffUserOrReadOnly
from .serializers import MovieSerializer


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

    def post(self, request, title):
        with transaction.atomic():
            response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey=9a6fa81f').json()

            error = response.get('Error')
            if error:
                return Response(
                    {'error': error},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Movie.objects.get_or_create(
                title=response.get('Title'),
                year=int(response.get('Year')),
                genre=response.get('Genre').split(", "),
                rating=float(response.get('imdbRating')),
                director=response.get('Director'),
                actors=response.get('Actors').split(", "),
                plot=response.get('Plot'),
                poster=response.get('Poster'),
                runtime=int(response.get('Runtime').replace(" min", "")),
                country=response.get('Country'),
                production=response.get('Production'),
            )

            return Response(
                {'success': f'Successfully created {title} movie.'},
                status=status.HTTP_200_OK
                )
     


class CreateMovieListAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request, limit=20):
        if limit > 20:
            limit = 20
        with transaction.atomic():
            response = requests.get(f'https://freetestapi.com/api/v1/movies?limit={limit}').json()
            for movie in response:
                title = movie.get('title')
                year = movie.get('year')
                response_2 = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f').json()
                Movie.objects.get_or_create(
                    title=title,
                    year=year,
                    genre=movie.get('genre'),
                    rating=movie.get('rating'),
                    director=movie.get('director'),
                    actors=movie.get('actors'),
                    plot=movie.get('plot'),
                    poster=response_2.get('Poster'),
                    runtime=movie.get('runtime'),
                    country=movie.get('country'),
                    production=movie.get('production'),
                )

            return Response(
                {'success': f'Successfully created {limit} movies.'},
                status=status.HTTP_200_OK
            )
        