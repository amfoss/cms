from django.core.management.base import BaseCommand
from datetime import date, datetime, timedelta
from members.models import Profile
from status.models import Log, Thread
from django.core.mail import EmailMultiAlternatives, send_mail
from framework import settings
from django.utils.html import strip_tags

from status.management.gmailFetcher import fetchStatusLog
from status.management.reportMaker import generateReport

from_email = settings.EMAIL_HOST_USER
now = datetime.now()
day = now.strftime("%w")
time = now.strftime("%H%M")

def generateThread(thread):
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

def logStatus(thread):
    d = date.today()
    if thread.generationTime > thread.logTime:
        d = d - timedelta(days=1)
    subject = thread.name + ' [%s]' % d.strftime('%d-%m-%Y')

    log = fetchStatusLog(d, subject)
    profiles = Profile.objects.filter(email__in=log.emails)

    MembersSentCount = 0
    for profile in profiles:
        if profile.user.is_active:
            Log.objects.create(
                member=profile.user,
                timestamp=log.members[profile.email],
                thread=thread
            )
            MembersSentCount += 1

    if thread.sendReport:
       sendReport(thread, log, MembersSentCount, d)

def sendReport(thread, log, MembersSentCount, d):
    d = now
    if thread.generationTime > thread.logTime:
        d = d - timedelta(days=1)

    genTime = thread.generationTime
    mint = d.replace(hour=int(genTime[:2]), minute=int(genTime[2:]))

    dueTime = thread.dueTime
    maxt = d.replace(hour=int(dueTime[:2]), minute=int(dueTime[2:]))

    print(mint)
    print(maxt)

    groupID = thread.telegramGroupID

    generateReport(d, log, MembersSentCount, mint, maxt, thread, groupID)


class Command(BaseCommand):
    help = 'Run Status Cron Jobs'

    def handle(self, *args, **options):

        # SENDS STATUS UPDATE THREAD VIA GMAIL
        threads = Thread.objects.filter(isActive=True, generationTime=time, days__contains=day)
        for thread in threads:
            generateThread(thread)

        # LOG STATUS UPDATES & SENDS TELEGRAM REPORT
        threads = Thread.objects.filter(isActive=True, logTime=time, days__contains=day)
        for thread in threads:
            logStatus(thread)
