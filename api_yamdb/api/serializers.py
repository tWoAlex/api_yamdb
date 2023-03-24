from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Review, Comment


"""
Это расчет рейтинга, его необходимо добавить в сериализатор заголовка
"""


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
