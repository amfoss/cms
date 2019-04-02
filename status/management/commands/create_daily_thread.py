from django.core.management.base import BaseCommand
from status.management.fetch_status_updates import DailyStatus
from datetime import date
from members.models import Profile
from status.models import StatusRegister
from django.core.mail import EmailMultiAlternatives, send_mail
from framework import settings


class Command(BaseCommand):
    help = 'Creates Status Update Thread'

    def handle(self, *args, **options):
        mailing_list = settings.MAILING_LIST
        from_email = settings.EMAIL_HOST_USER

        subject = 'Status Update [%s]' % date.today().strftime('%d-%m-%Y')

        text_content = 'Please reply to this thread to send your status ' \
                       'updates for %s' % date.today().strftime('%d-%m-%Y')

        send_mail(
            subject,
            text_content,
            from_email,
            [mailing_list],
            fail_silently=False,
        )
