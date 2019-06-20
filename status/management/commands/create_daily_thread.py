from django.core.management.base import BaseCommand
from status.management.fetch_status_updates import DailyStatus
from datetime import date
from members.models import Profile
from status.models import StatusRegister
from django.core.mail import EmailMultiAlternatives, send_mail
from framework import settings
from django.utils.html import strip_tags


class Command(BaseCommand):
    help = 'Creates Status Update Thread'

    def handle(self, *args, **options):
        mailing_list = settings.MAILING_LIST
        from_email = settings.EMAIL_HOST_USER

        subject = 'Status Update [%s]' % date.today().strftime('%d-%m-%Y')

        with open("thread_text.txt") as file:
            message = file.read()

        plain_message = strip_tags(message)
        send_mail(
            subject,
            plain_message,
            from_email,
            [mailing_list],
            html_message=message,
            fail_silently=False,
        )
