import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from college.models import Profile

class Command(BaseCommand):
    help = 'imports user data into a csv file'

    def handle(self, *args, **options):
        with open('student_data.csv', 'rt') as f:
            data = csv.reader(f)
            for row in data:
                username = row[0]
                admissionYear = row[1]
                branch = row[2]
                classSection = row[3]
                rollNo = row[4]
                user = User.objects.get(username=username)
                obj, created = Profile.objects.get_or_create(
                    user=user,
                    admissionYear=admissionYear
                )
                obj.admissionYear = admissionYear
                obj.classSection = classSection
                obj.branch = branch
                obj.rollNo = rollNo
                obj.save()

