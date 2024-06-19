# your_app/serializers.py
from djoser.serializers import UserSerializer
from .models import TunedUser


""" class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = TunedUser
        fields = ('id', 'email', 'password') """


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = TunedUser
        fields = ('id', 'email')
