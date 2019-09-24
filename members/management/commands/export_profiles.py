import csv
from django.core.management.base import BaseCommand
from ...models import Profile

class Command(BaseCommand):
    help = 'Exports profile data into a csv file'

    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        profileData = []
        for profile in profiles:
            profileArr = []
            profileArr.append(profile.user.username)
            profileArr.append(profile.email)
            profileArr.append(profile.first_name)
            profileArr.append(profile.last_name)
            profileArr.append(profile.batch)
            profileData.append(profileArr)

        with open('profiles.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(profileData)
        csvFile.close()

