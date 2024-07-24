from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.db.models import Exists, OuterRef, Prefetch, Q, Avg
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from itertools import chain
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import TunedUser, UserRatingActivity, UserFavoriteActivity, UserReviewActivity, UserWatchLaterActivity
from .serializers import CustomUserSerializer
from .forms import UserCreateForm, UserUpdateForm, UserLoginForm
from .permissions import UserPermission
from apps.movies.models import MovieRating, MovieReview, FavMovie


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = TunedUser.objects.filter(is_staff=False).order_by('-pk')
    serializer_class = CustomUserSerializer
    permission_classes = [UserPermission]
    pagination_class = ListPagination


class UserListView(generic.ListView):
    model = TunedUser
    context_object_name = 'users'
    paginate_by = 15
    template_name = "users/list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(is_staff=False)

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
    template_name = 'users/detail.html'

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
        qs = super().get_queryset().prefetch_related(prefetch_favs, prefetch_reviews, prefetch_ratings).filter(is_staff=False)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """ movies = Movie.objects.annotate(
                is_saved=Exists(FavMovie.objects.filter(movie=OuterRef('pk'), user=self.object)),
                is_reviewed=Exists(MovieReview.objects.filter(movie=OuterRef('pk'), user=self.object)),
                user_rating=Avg('rating_movie_set__rating', filter=Q(rating_movie_set__user=self.object))
            ).filter(Q(is_saved=True) | Q(is_reviewed=True) | Q(user_rating__isnull=False)) """

        """ context['movies'] = movies """

        user = self.object
        
        user_favorite_activity = UserFavoriteActivity.objects.prefetch_related('favorite__movie').filter(user=user)
        user_review_activity = UserRatingActivity.objects.select_related('rating__movie').filter(user=user)
        user_rating_activity = UserReviewActivity.objects.select_related('review__movie').filter(user=user)
        user_wl_activity = UserWatchLaterActivity.objects.select_related('wl__movie').filter(user=user)

        ratings_count = MovieRating.objects.filter(user=user).count()
        reviews_count = MovieReview.objects.filter(user=user).count()
        favorites_count = FavMovie.objects.filter(user=user).count()

        context['ratings_count'] = ratings_count
        context['reviews_count'] = reviews_count
        context['favorites_count'] = favorites_count
        context['films_count'] = ratings_count + ratings_count + favorites_count
        context['activities'] = sorted(chain(user_favorite_activity, user_review_activity, user_rating_activity, user_wl_activity), key=lambda x: x.created_at, reverse=True)

        return context


class UserUpdateView(generic.UpdateView):
    model = TunedUser
    form_class = UserUpdateForm
    template_name = 'users/update.html'

    def get_object(self, queryset=None):
        user = super().get_queryset().get(pk=self.request.user.pk)

        return user

    def form_valid(self, form):
        messages.success(self.request, 'Profile has been updated.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


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

