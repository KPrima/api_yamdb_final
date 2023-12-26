import datetime as dt

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username
from .constants import (
    MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
)


User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        required=True,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True
    )

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            existing_user = User.objects.filter(username=username).exists()
            if existing_user:
                raise ValidationError({'username': ['Этот логин уже занят']})

            existing_email = User.objects.filter(email=email).exists()
            if existing_email:
                raise ValidationError(
                    {'email': ['Этот адрес эл.почты уже занят']}
                )
            if existing_user and existing_email:
                raise ValidationError({
                    'username': ['Этот логин уже занят'],
                    'email': ['Этот адрес эл.почты уже занят']
                })

        return user

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        required=True,
        validators=[validate_username, ]
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'role',
            'email',
            'bio',
        ]


class UserUpdateSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть позже текущего'
            )
        return value

    def to_representation(self, value):
        return TitleSerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        default=0, read_only=True, source='average_score'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context.get('request').user
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Нельзя оставить больше 1 отзыва!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
