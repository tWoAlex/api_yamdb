from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryFromSlugSerializer(CategorySerializer):
    def to_internal_value(self, data):
        return Category.objects.get(slug=data)


class GenreFromSlugSerializer(CategorySerializer):
    def to_internal_value(self, data):
        return Genre.objects.get(slug=data)


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryFromSlugSerializer()
    genre = GenreFromSlugSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, attrs):
        print('\n\n\n\n\n')
        print(attrs)
        print('\n\n\n\n\n')
        return attrs

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = super().create(validated_data)
        for genre in genres:
            GenreTitle.objects.get_or_create(
                genre=genre, title=title,)
        return title
