import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Exports user model data as csv'

    def handle(self, *args, **options):
        users = User.objects.all()
        usersData = []
        for user in users:
            userArr = []
            userArr.append(user.username)
            userArr.append(user.email)
            userArr.append(user.first_name)
            userArr.append(user.last_name)
            usersData.append(userArr)

        with open('users.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(usersData)
        csvFile.close()

