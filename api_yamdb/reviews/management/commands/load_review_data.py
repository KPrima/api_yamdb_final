from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = "Загрузка данных из файла review.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/review.csv')):
            title = get_object_or_404(Title, pk=row['title_id'])
            author = get_object_or_404(User, pk=row['author'])
            review = Review.objects.create(
                id=row['id'],
                title=title,
                text=row['text'],
                score=row['score'],
                author=author,
                pub_date=row['pub_date'],
            )
            review.save()
