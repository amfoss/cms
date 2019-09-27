from django.core.management.base import BaseCommand
from status.models import Log

class Command(BaseCommand):
    help = 'Logs Daily Status Updates'

    def handle(self, *args, **options):
        Log.objects.all().delete()