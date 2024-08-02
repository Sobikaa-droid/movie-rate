from rest_framework import serializers

from .models import Movie, MovieRating, MovieReview, FavMovie, MovieWatchLater


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        additional_info = self.context.get('additional_info', {})
        representation.update(additional_info)

        return representation


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


class RatingModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieRating
        fields = '__all__'
        read_only_fields = ['creation_date']


class FavoriteModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = FavMovie
        fields = '__all__'
        read_only_fields = ['creation_date']


class ReviewModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieReview
        fields = '__all__'
        read_only_fields = ['creation_date']


class WatchLaterModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieWatchLater
        fields = '__all__'
        read_only_fields = ['creation_date']
