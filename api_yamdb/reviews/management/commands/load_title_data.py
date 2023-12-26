from csv import DictReader

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, GenreTitle, Title


class Command(BaseCommand):
    help = "Загрузка данных из файла titles.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/titles.csv')):
            category = get_object_or_404(Category, pk=row['category'])
            title, status = Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category
            )
            title.save()

        for row in DictReader(open('static/data/genre_title.csv')):
            title = get_object_or_404(Title, pk=row['title_id'])
            genre = get_object_or_404(Genre, pk=row['genre_id'])
            GenreTitle.objects.create(title=title, genre=genre)
