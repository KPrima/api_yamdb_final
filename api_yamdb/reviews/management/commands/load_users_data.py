from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Загрузка данных из файла users.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/users.csv')):
            user, status = User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()
