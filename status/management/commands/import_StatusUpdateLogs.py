import csv
from django.core.management.base import BaseCommand
import dateutil.parser
from django.contrib.auth.models import User
from status.models import Thread, Log

class Command(BaseCommand):
    help = 'Imports Status Update Log data from a csv file'

    def handle(self, *args, **options):
        with open('StatusUpdateLogs.csv', 'rt') as f:
            data = csv.reader(f)
            for row in data:
                user = User.objects.get(username=row[0])
                timestamp = dateutil.parser.parse(row[1])
                thread = Thread.objects.get(id=row[2])
                logDate = dateutil.parser.parse(row[3]).date()

                obj, created = Log.objects.get_or_create(
                    member=user,
                    date=logDate,
                    timestamp=timestamp,
                    thread=thread
                )
                obj.save()


