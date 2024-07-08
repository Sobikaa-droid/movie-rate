from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import TunedUser
from .serializers import CustomUserSerializer
from .forms import UserCreateForm, UserUpdateForm, UserLoginForm
from .permissions import UserPermission


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
        qs = super().get_queryset().filter(is_staff=False)

        return qs


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

