import telegram
from django.core.management.base import BaseCommand
from status.management.fetch_status_updates import DailyStatus
from datetime import date, datetime, timedelta
from members.models import Profile
from status.models import Log
from framework import settings
from django.utils import timezone

class Command(BaseCommand):
    help = 'Logs Daily Status Updates'

    def add_arguments(self, parser):
        parser.add_argument('day', nargs='?', type=int)
        parser.add_argument('month', nargs='?', type=int)
        parser.add_argument('year', nargs='?', type=int)

    def handle(self, *args, **options):
        d = date.today()

        # Checks if specific date to fetch status update is provided
        if options['day'] and options['month'] and options['year']:
            d = date(options['year'], options['month'], options['day'])


        StartTime = timezone.make_aware(datetime.combine(d, datetime.min.time()))
        EndTime = timezone.make_aware(datetime.combine(d, datetime.max.time()))
        print(StartTime)
        print(EndTime)

        StartCount = Log.objects.filter(timestamp__gt=StartTime, timestamp__lt=EndTime).count()
        Log.objects.filter(timestamp__gt=StartTime, timestamp__lt=EndTime).delete()
        EndCount = Log.objects.filter(timestamp__gt=StartTime, timestamp__lt=EndTime).count()

        if EndCount == 0:
            print(str(StartCount) + " status logs successfully deleted from " + str(d))
        else:
            print("Could not delete.")
