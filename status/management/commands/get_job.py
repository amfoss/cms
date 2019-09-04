from django.core.management.base import BaseCommand
from datetime import date, datetime, timedelta
from members.models import Profile, Group
from status.models import Log, Thread
from django.core.mail import EmailMultiAlternatives, send_mail
from framework import settings
from django.utils.html import strip_tags
from django.utils import timezone

from attendance.generateSSID import refreshSSID

from status.gmailFetcher import fetchStatusLog
from status.reportMaker import generateReport

to_tz = timezone.get_default_timezone()

from_email = settings.EMAIL_HOST_USER

now = datetime.now().astimezone(to_tz)
day = now.strftime("%w")
time = now.strftime("%H%M")


def generateSSIDName():
    groups = Group.objects.filter(attendanceEnabled=True)
    for group in groups:
        refreshSSID(group.attendanceThread)

def getThreadDateTime(thread):
    d = now
    if thread.generationTime > thread.logTime:
        d = d - timedelta(days=1)
    return d

def calcMinTime(thread):
    genTime = thread.generationTime
    d = getThreadDateTime(thread)
    return d.replace(hour=int(genTime[:2]), minute=int(genTime[2:]))

def calcMaxTime(thread):
    dueTime = thread.dueTime
    d = getThreadDateTime(thread)
    return d.replace(hour=int(dueTime[:2]), minute=int(dueTime[2:]))

def generateThread(thread):
    send_mail(
        thread.name + ' [%s]' % now.strftime('%d-%m-%Y'),
        strip_tags(thread.threadMessage),
        from_email,
        [Group.objects.get(thread=thread).email],
        html_message=thread.threadMessage,
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
            mint = calcMinTime(thread)
            query = Log.objects.filter(member=profile.user, timestamp__gte=mint, thread=thread)
            if query.count() == 0:
                Log.objects.create(
                    member=profile.user,
                    timestamp=log.members[profile.email],
                    thread=thread
                )
            MembersSentCount += 1

    if thread.enableGroupNotification:
       sendReport(thread, log, MembersSentCount, d)

def sendReport(thread, log, MembersSentCount, d):
    mint = calcMinTime(thread)
    maxt = calcMaxTime(thread)

    generateReport(d, log, MembersSentCount, mint, maxt, thread)


class Command(BaseCommand):
    help = 'Run Status Cron Jobs'

    def handle(self, *args, **options):

        # REGENERATE WIFI NAME
        generateSSIDName()

        # SENDS STATUS UPDATE THREAD VIA GMAIL
        threads = Thread.objects.filter(enabled=True, generationTime=time, days__contains=day)
        for thread in threads:
            generateThread(thread)

        # LOG STATUS UPDATES & SENDS TELEGRAM REPORT
        threads = Thread.objects.filter(enabled=True, logTime=time, days__contains=day)
        for thread in threads:
            logStatus(thread)
