from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', views.UserAPIViewSet, basename="users")

urlpatterns = [
    # api
    path('api/', include(router.urls)),
    # generic
    path('', views.UserListView.as_view(), name='list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', login_required(views.UserUpdateView.as_view(), login_url='users:register'), name='update'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', login_required(views.LogoutView.as_view(), login_url='users:register'), name='logout'),
]