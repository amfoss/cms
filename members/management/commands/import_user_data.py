import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'imports user data into a csv file'

    def handle(self, *args, **options):
        with open('user_data.csv', 'rt') as f:
            data = csv.reader(f)
            for row in data:
                username = row[0]
                email = row[1]
                first_name = row[2]
                last_name = row[3]
                obj, created = User.objects.get_or_create(
                    username=username
                )
                obj.email = email
                obj.first_name = first_name
                obj.last_name = last_name
                obj.save()

