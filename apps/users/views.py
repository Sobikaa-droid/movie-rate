from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch, Q, Avg
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from itertools import chain
import requests

from .models import TunedUser, Country, UserFavoriteActivity, UserRatingActivity, UserReviewActivity, UserWatchLaterActivity
from .serializers import CustomUserSerializer
from .forms import UserCreateForm, UserUpdateForm, UserLoginForm
from . import custom_permissions
from apps.movies.models import MovieRating, MovieReview, FavMovie, Movie, MovieWatchLater


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = TunedUser.objects.order_by('-pk')
    serializer_class = CustomUserSerializer
    permission_classes = [custom_permissions.IsAuthenticatedAndUserOrReadOnly]
    pagination_class = ListPagination


class UserListView(generic.ListView):
    model = TunedUser
    context_object_name = 'users'
    paginate_by = 15
    template_name = "users/users.html"

    def get_queryset(self):
        qs = super().get_queryset()

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


class UserDetailView(generic.DetailView):
    model = TunedUser
    context_object_name = 'user'
    template_name = 'users/user_base.html'

    def get_queryset(self):
        prefetch_favs = Prefetch(
            'fav_user_set',
            queryset=FavMovie.objects.select_related("movie")
        )
        prefetch_reviews = Prefetch(
            'review_user_set',
            queryset=MovieReview.objects.select_related("movie")
        )
        prefetch_ratings = Prefetch(
            'rating_user_set',
            queryset=MovieRating.objects.select_related("movie")
        )
        qs = super().get_queryset().prefetch_related(
            prefetch_favs,
            prefetch_reviews,
            prefetch_ratings
            ).all().distinct('id')

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object

        films = Movie.objects.annotate(
                is_saved=Exists(FavMovie.objects.filter(movie=OuterRef('pk'), user=user)),
                is_reviewed=Exists(MovieReview.objects.filter(movie=OuterRef('pk'), user=user)),
                user_rating=Avg('rating_movie_set__rating', filter=Q(rating_movie_set__user=user))
            ).filter(Q(is_saved=True) | Q(is_reviewed=True) | Q(user_rating__isnull=False))
        
        user_favorite_activity = user.favorite_activity_user_set.select_related('favorite__movie')
        user_review_activity = user.rating_activity_user_set.select_related('rating__movie')
        user_rating_activity = user.review_activity_user_set.select_related('review__movie')
        user_wl_activity = user.wl_activity_user_set.select_related('wl__movie')

        context['films_count'] = films.count()
        context['activities'] = sorted(
            chain(user_favorite_activity, 
                  user_review_activity, 
                  user_rating_activity, 
                  user_wl_activity), 
            key=lambda x: x.created_at, reverse=True)[:5]
        context['template'] = 'users/user_profile.html'

        return context
    

class UserUpdateView(generic.UpdateView):
    form_class = UserUpdateForm
    template_name = 'users/update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserObjectsListViewBase(generic.ListView):
    context_object_name = 'qs'
    template_name = 'users/user_base.html'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().select_related('user', 'movie').filter(user__pk=self.kwargs.get('user_pk'))
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(TunedUser.objects.distinct('id'), pk=self.kwargs.get('user_pk'))
        films = Movie.objects.annotate(
                is_saved=Exists(FavMovie.objects.filter(movie=OuterRef('pk'), user=user)),
                is_reviewed=Exists(MovieReview.objects.filter(movie=OuterRef('pk'), user=user)),
                is_rated=Exists(MovieRating.objects.filter(movie=OuterRef('pk'), user=user))
            ).filter(Q(is_saved=True) | Q(is_reviewed=True) | Q(is_rated=True))
        
        context['user'] = user
        context['films_count'] = films.count()

        return context
    

class UserActivityView(UserObjectsListViewBase):
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')

        user_favorite_activity = UserFavoriteActivity.objects.filter(
            user__pk=user_pk).select_related('favorite__movie')
        user_review_activity = UserRatingActivity.objects.filter(
            user__pk=user_pk).select_related('rating__movie')
        user_rating_activity = UserReviewActivity.objects.filter(
            user__pk=user_pk).select_related('review__movie')
        user_wl_activity = UserWatchLaterActivity.objects.filter(
            user__pk=user_pk).select_related('wl__movie')

        activity_objects = sorted(
            chain(user_favorite_activity, 
                  user_review_activity, 
                  user_rating_activity, 
                  user_wl_activity), 
            key=lambda x: x.created_at, reverse=True)

        return activity_objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'users/user_activity.html'
        return context


class UserFavoritesView(UserObjectsListViewBase):
    model = FavMovie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'users/user_favorites.html'
        return context
    

class UserWatchLaterView(UserObjectsListViewBase):
    model = MovieWatchLater

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'users/user_wls.html'
        return context
    

class UserRatingsView(UserObjectsListViewBase):
    model = MovieRating
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'users/user_ratings.html'
        return context


class UserReviewsView(UserObjectsListViewBase):
    model = MovieReview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'users/user_reviews.html'
        return context


class UserRegisterView(generic.FormView):
    form_class = UserCreateForm
    success_url = reverse_lazy('home')
    template_name = 'users/auth.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='apps.users.auth_backend.EmailBackend')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_type'] = 'Register'

        return context


class UserLoginView(generic.FormView):
    form_class = UserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'users/auth.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_type'] = 'Login'

        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class CreateCountryListAPIView(APIView):
    permission_classes = [custom_permissions.IsStaffUser]

    def post(self, request):
        with transaction.atomic():
            response = requests.get('https://restcountries.com/v3.1/all')
            response_data = {}

            if response.status_code != 200:
                return Response(
                    {'error': response.status_code},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            response = response.json()
            
            for lst in response:
                common_name = lst.get('name').get('common')
                cca2 = lst.get('cca2')
                obj, created = Country.objects.get_or_create(
                        common_name=common_name,
                        cca2=cca2,
                    )
                if created:
                    response_data.update({cca2: 'created'})
                else:
                    response_data.update({cca2: 'exists'})

            return Response(
                {'success': response_data},
                status=status.HTTP_200_OK
            )    
