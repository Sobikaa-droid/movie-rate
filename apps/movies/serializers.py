from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    year = serializers.IntegerField(required=False)


class MovieCreateListSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        required=True,
        min_value=2,
        max_value=25,
        error_messages={
            'min_value': 'The limit must be at least %(limit_value)s.',
            'max_value': 'The limit must not exceed %(limit_value)s.'
        }
    )
