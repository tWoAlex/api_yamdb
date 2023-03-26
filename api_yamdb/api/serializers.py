from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryFromSlugRelatedField(serializers.SlugRelatedField,
                                   CategorySerializer):
    queryset = Category.objects.all()
    to_representation = CategorySerializer.to_representation


class GenreFromSlugRelatedField(serializers.SlugRelatedField,
                                GenreSerializer):
    queryset = Genre.objects.all()
    to_representation = GenreSerializer.to_representation


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryFromSlugRelatedField(slug_field='slug')
    genre = GenreFromSlugRelatedField(slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def to_internal_value(self, data):
        print()
        print('-' * 60)
        for key, value in data.items():
            print(f'{key}: {value} ({type(value)})')
        print('-' * 60)
        print()
        try:
            return super().to_internal_value(data)
        except Exception as exc:
            print()
            print('-' * 60)
            print(type(exc))
            print(exc)
            print('-' * 60)
            print()


def get_rating(self, obj):
    rating = obj.reviews.aggregate(
        Avg('score')).get('score__avg')
    return round(rating, 2) if rating else rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    score = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'На одно произведение можно оставлять только один отзыв'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class RegistrationSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError('Никнейм "me" запрещён')
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenAproveSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
