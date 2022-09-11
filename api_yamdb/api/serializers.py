from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg

from reviews.models import Comment, Review, Title, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    # title = serializers.HiddenField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['title_id', 'author'],
        #         message='На одно произведение пользователь может оставить один отзыв!'
        #     )
        # ]
        read_only_fields = ('pub_date',)

    # def validate(self, data):
    #     # author = self.context['request'].user
    #     # title = self.context['request'].title_id
    #     if Review.objects.filter(
    #         author_username=data['author'], title=data['title']
    #     ).exists():
    #         raise serializers.ValidationError(
    #             'На одно произведение пользователь может оставить один отзыв!'
    #         )
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    # category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return Title.objects.get(name=obj.name).reviews.aggregate(
            rating=Avg("score")
        )['rating']
