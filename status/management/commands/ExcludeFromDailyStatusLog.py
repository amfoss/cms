from django.core.management.base import BaseCommand
from datetime import datetime
from status.models import DailyLog
from members.models import Group


class Command(BaseCommand):
    help = 'Exclude Members from StatusLogs'

    def handle(self, *args, **options):
        members = []
        for group in Group.objects.exclude(id=4).all():
            for member in group.members.all():
                members.append(member)

        start = datetime.strptime("11-08-2019", '%d-%m-%Y').date()
        end = datetime.strptime("04-10-2019", '%d-%m-%Y').date()

        logs = DailyLog.objects.filter(date__gte=start, date__lte=end)

        for log in logs:
            log.didNotSend.remove(*members)
            log.late.remove(*members)
            log.members.remove(*members)
