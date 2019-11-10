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


def getSubject(thread, d):
    return thread.name + ' [%s]' % d.strftime('%d-%m-%Y')


#
#
# Generating Status Update Thread
#
#

def generateThread(thread, email):
    send_mail(
        getSubject(thread, now),
        strip_tags(thread.threadMessage),
        from_email,
        [email],
        html_message=thread.threadMessage,
        fail_silently=False,
    )

#
#
# Logging Status Updates
#
#


def logStatus(thread):
    d = date.today()
    if thread.generationTime > thread.logTime:
        d = d - timedelta(days=1)

    subject = getSubject(thread,d)

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
                    date=mint.date(),
                    thread=thread
                )
            MembersSentCount += 1

    if thread.enableGroupNotification:
       sendReport(thread, log, MembersSentCount, d)

#
#
# Reporting Status Updates
#
#


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

def sendReport(thread, log, MembersSentCount, d):
    mint = calcMinTime(thread)
    maxt = calcMaxTime(thread)

    generateReport(d, log, MembersSentCount, mint, maxt, thread)


class Command(BaseCommand):
    help = 'Runs all tasks of CMS required to be done at the moment'

    def handle(self, *args, **options):

        # get all groups
        groups = Group.objects.all()

        # for each group
        for group in groups:

            # If the group has attendance enabled
            if group.attendanceEnabled:

                # generate new SSID name if refreshing is required
                refreshSSID(group.attendanceModule)

            # If the group has Status Update Enabled
            if group.statusUpdateEnabled:

                # If today is an active day
                if day in group.thread.days:

                    # If its the generation time
                    if group.thread.generationTime == time:
                        # generate new thread for the group
                        generateThread(group.thread, group.email)

                    # If its the logging time
                    if group.thread.logTime == time:
                        # log status updates from the group's thread
                        logStatus(group.thread)
