from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
import requests

from .models import Movie
from .permissions import IsStaffUser, IsStaffUserOrReadOnly
from .serializers import MovieSerializer, MovieCreateSerializer, MovieCreateListSerializer


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
                        year=int(response.get('Year', '0')[0:4]) if response.get('Year') != 'N/A' else 0,
                        genre=response.get('Genre', 'N/A').split(", "),
                        rating=float(response.get('imdbRating', 0)) if response.get('imdbRating') != 'N/A' else float(0),
                        director=response.get('Director', 'N/A'),
                        actors=response.get('Actors', 'N/A').split(", "),
                        plot=response.get('Plot', 'N/A'),
                        poster=response.get('Poster', 'N/A'),
                        runtime=int(response.get('Runtime', '0').replace(" min", "")) if response.get('Runtime') != 'N/A' else 0,
                        country=response.get('Country', 'N/A'),
                        production=response.get('Production', 'N/A'),
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
                limit = serializer.validated_data.get('limit')
                response = requests.get(f'https://freetestapi.com/api/v1/movies?limit={limit}').json()
                for movie in response:
                    title = movie.get('title')
                    year = movie.get('year')
                    response_2 = requests.get(f'https://www.omdbapi.com/?t={title}&year={year}&apikey=9a6fa81f').json()
                    Movie.objects.get_or_create(
                        title=title,
                        year=year,
                        genre=movie.get('genre', 'N/A'),
                        rating=movie.get('rating', 0) if movie.get('rating') != 'N/A' else 0,
                        director=movie.get('director', 'N/A'),
                        actors=movie.get('actors', 'N/A'),
                        plot=movie.get('plot', 'N/A'),
                        poster=response_2.get('Poster', 'N/A'),
                        runtime=movie.get('runtime', 0) if movie.get('runtime') != 'N/A' else 0,
                        country=movie.get('country', 'N/A'),
                        production=movie.get('production', 'N/A'),
                    )

                return Response(
                    {'success': f'Successfully created {limit} movies.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        