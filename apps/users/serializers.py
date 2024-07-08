# your_app/serializers.py
from rest_framework import serializers
from .models import TunedUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TunedUser
        fields = ['id', 'email', 'username', 'password', 'first_name', 'second_name', 'description', 'country', 'year_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = TunedUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        # Update racer instances with the validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.description = validated_data.get('description', instance.description)
        instance.year_of_birth = validated_data.get('year_of_birth', instance.year_of_birth)
        instance.country = validated_data.get('country', instance.year_of_birth)

        # Check if password is provided and update it if necessary
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
