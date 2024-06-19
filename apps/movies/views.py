from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .models import Movie
from .permissions import IsStaffUser


class CreateMovieListAPIView(APIView):
    permission_classes = [IsStaffUser]

    # 20 is the maximum limit
    def post(self, request, limit=20):
        with transaction.atomic():
            response = requests.get(f'https://freetestapi.com/api/v1/movies?limit={limit}')
            for movie in response.json():
                Movie.objects.get_or_create(
                    title=movie.get('title'),
                    year=movie.get('year'),
                    genre=movie.get('genre'),
                    rating=movie.get('rating'),
                    director=movie.get('director'),
                    actors=movie.get('actors'),
                    plot=movie.get('plot'),
                    poster=movie.get('poster'),
                    runtime=movie.get('runtime'),
                    country=movie.get('country'),
                    production=movie.get('production'),
                )

            return Response(
                {'success': f'Successfully created {limit} movies.'},
                status=status.HTTP_200_OK
            )