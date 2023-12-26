from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    help = "Загрузка данных из файла genre.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/genre.csv')):
            genre, status = Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()
