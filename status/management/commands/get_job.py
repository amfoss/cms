from django.core.management.base import BaseCommand
from datetime import date, datetime
from members.models import Profile
from status.models import StatusRegister, Thread
from django.core.mail import EmailMultiAlternatives, send_mail
from framework import settings
from django.utils.html import strip_tags

from status.management.gmailFetcher import DailyStatus
from status.management.reportMaker import sendReport


def sendThreads():
    from_email = settings.EMAIL_HOST_USER
    now = datetime.now()
    day = now.strftime("%w")
    time = now.strftime("%H%M")
    threads = Thread.objects.filter(isActive=True, generationTime=time)
    for thread in threads:
        days = thread.days.split(',')
        if day in days:
            subject = thread.name + ' [%s]' % now.strftime('%d-%m-%Y')
            message = strip_tags(thread.threadMessage)
            mailing_list = thread.threadEmail
            send_mail(
                subject,
                message,
                from_email,
                [mailing_list],
                html_message=message,
                fail_silently=False,
            )

def logMails():
    now = datetime.now()
    day = now.strftime("%w")
    time = now.strftime("%H%M")
    threads = Thread.objects.filter(isActive=True, logTime=time)
    for thread in threads:
        days = thread.days.split(',')
        if day in days:
            subject = thread.name + ' [%s]' % now.strftime('%d-%m-%Y')
            d = date.today() - timedelta(days=1)
            logs = DailyStatus(d,subject)
            profiles = Profile.objects.filter(email__in=logs.emails)

            MembersSentCount = 0
            for profile in profiles:
                if profile.user.is_active:
                    StatusRegister.objects.create(
                        member=profile.user,
                        timestamp=logs.members[profile.email],
                        thread=thread
                    )
                    MembersSentCount += 1

def sendReports():
    now = datetime.now()
    day = now.strftime("%w")
    time = now.strftime("%H%M")
    threads = Thread.objects.filter(isActive=True, logTime=time)
    for thread in threads:
        days = thread.days.split(',')
        if day in days:
            d = date.today() - timedelta(days=1)
            day = datetime.combine(d, datetime.min.time())

            genTime = thread.generationTime
            mint = day.replace(hour=genTime[:2], minute=genTime[2:])
            dueTime = thread.dueTime
            maxt = day.replace(hour=dueTime[:2], minute=dueTime[2:])
            groupID = thread.telegramGroupID

            sendReports(mint,maxt,thread,groupID)

class Command(BaseCommand):
    help = 'Get Jobs'

    def handle(self, *args, **options):
        sendThreads()
        logMails()
        sendReports()
