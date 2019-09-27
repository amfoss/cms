import csv
from django.core.management.base import BaseCommand
from io import StringIO
from django.core.mail import EmailMessage

from framework import settings
from ...models import Log

from_email = settings.EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'Exports & Sends Status Update Log data to an email as a CSV'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        logs = Log.objects.all()
        logData = []
        logData.append(['username', 'timestamp', 'thread id', 'due time'])
        for log in logs:
            logRow = []
            logRow.append(log.member.username)
            logRow.append(log.timestamp)
            logRow.append(log.thread.id)
            logRow.append(log.thread.dueTime)
            logData.append(logRow)

        csvfile = StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(logData)

        email = EmailMessage(
            "Status Update Log Backup",
            'Please find the attachment.',
            from_email,
            [email],
        )
        email.attach('StatusUpdateLogs.csv', csvfile.getvalue(), 'text/csv')
        email.send()

