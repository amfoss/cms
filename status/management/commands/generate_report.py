from django.core.management.base import BaseCommand
from datetime import date, timedelta

from crons.StatusUpdateReporter import TelegramReporter


class Command(BaseCommand):
    help = 'Runs all tasks of CMS required to be done at the moment'

    def handle(self, *args, **options):
        d = date.today() - timedelta(days=2)
        print()
