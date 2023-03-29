import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import (Category, Genre, Title, GenreTitle,
                            Review, Comment, User)


DIR = settings.STATICFILES_DIRS[0] / 'data'
MODEL_TO_FILE = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv'
}

for key in MODEL_TO_FILE:
    MODEL_TO_FILE[key] = DIR / MODEL_TO_FILE[key]


class Command(BaseCommand):
    help = "Loads data from static/data/*.csv"

    def handle(self, *args, **options):
        for model, filepath in MODEL_TO_FILE.items():
            with open(filepath, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # row.pop('id')
                    model.objects.create(**row)
