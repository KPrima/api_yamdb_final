from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Загрузка данных из файла comments.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/comments.csv')):
            review = get_object_or_404(Review, pk=row['review_id'])
            author = get_object_or_404(User, pk=row['author'])
            comment = Comment.objects.create(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date'],
            )
            comment.save()
