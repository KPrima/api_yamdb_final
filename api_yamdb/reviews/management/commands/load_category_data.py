from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = "Загрузка данных из файла category.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/category.csv')):
            category, status = Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()
