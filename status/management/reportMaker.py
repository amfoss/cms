import telegram
from datetime import date, datetime, timedelta
from members.models import Profile, Group
from status.models import Log
from framework import settings
from pytz import timezone
from operator import itemgetter


from pytz import timezone

def getPercentageSummary(Count, Total):
    if Count / Total >= 1:
        return 'Everyone has send their Status Updates today! &#128079;'
    elif Count / Total > 0.90:
        return 'More than 90% of members sent their status update today.'
    elif Count / Total > 0.75:
        return 'More than 75% of members sent their status update today.'
    elif Count / Total < 0.50:
        return 'Less than 50% of members sent their status update today.'
    elif Count / Total < 0.25:
        return 'Less than 25% of members sent their status update today.'
    elif Count / Total < 0.10:
        return 'Less than 10% of members sent their status update today.'
    return ''


def getName(first, last):
    name = first
    if last:
        name += ' ' + last
    return name

def getFirstPerson(updates):
    person = Profile.objects.get(user=updates[0].member)
    ft = updates[0].timestamp
    return getName(person.first_name, person.last_name) + ' (' + ft.astimezone(timezone('Asia/Kolkata')).strftime('%I:%M %p') + ')'

def getLastPerson(updates):
    return getFirstPerson(list(reversed(updates)))

def getLateLogs(thread, members, maxt):
    now = datetime.now()
    # Find status updates send between due time and now
    lateLogs = Log.objects.filter(timestamp__gt=maxt, timestamp__lt=now, thread=thread).order_by('timestamp')

    message = ''
    i = 0
    if lateLogs.count() > 0:
        message += '''\n\n<b>&#8987; LATE: </b> \n'''
        for m in members:
            obj = lateLogs.filter(member=m['user'])
            if obj:
                i = i + 1
                message += str(i) + '. ' + getName(m['first_name'], m['last_name']) +  ' [' + obj[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime('%I:%M %p') + '] \n'
    return message

def getBatchName(y):
    now = datetime.now()
    year = int(now.strftime("%Y"))
    if y == year:
        return 'First Year Batch'
    elif y+1 == year:
        return 'Second Year Batch'
    elif y+2 == year:
        return 'Third Year Batch'
    elif y+3 == year:
        return 'Fourth Year Batch'

def generateReport(d, log, MembersSentCount, mint, maxt, thread):

    groupMembers = Group.objects.filter(thread=thread).values('members')
    groupProfiles = Profile.objects.filter(user__in=groupMembers)
    MemberCount =  groupProfiles.count()

    # Get member profile data from CMS
    members_list = groupProfiles.values('user', 'first_name', 'last_name', 'email', 'batch').order_by('batch')

    # Get All Status Update Entries for the Day
    updates = Log.objects.filter(timestamp__gt=mint, timestamp__lt=maxt, thread=thread).order_by('timestamp')

    # Title for the Status Update Report for Telegram
    message = '<b>Daily Status Update Report</b> \n\n &#128197; ' + d.strftime(
        '%d %B %Y') + ' | &#128228; ' + str(MembersSentCount) + '/' + str(MemberCount) + ' Members'

    # Send summary based on percentage of members sending status updates
    message += '\n\n<b>' + getPercentageSummary(MembersSentCount,MemberCount) + '</b>'

    if updates.count() > 0:
        ## Add Names of First and Last Person to status updates to the message
        message += '\n\n<b>&#11088; First : </b>' + getFirstPerson(updates) + '\n'
        message += '<b>&#128012; Last : </b>' + getLastPerson(updates) + '\n'

    # Generate Report for members who have send status update lately
    message += getLateLogs(thread, members_list, maxt)

    # Reports are generated only for the last 4 batches from current year
    mf = 0  # member flag
    # For each year in last four years
    for y in range(d.year, d.year - 4, -1):
        # year flag
        yf = 0
        # counter for members
        i = 0
        # For each member in member list
        for m in members_list:
            if m['email'] not in log.emails and y == m['batch']:
                if not mf:
                    message += '''\n\n<b>&#128561; DID NOT SEND: </b> \n'''
                    mf = 1
                if not yf:
                    message += '\n<b>' + getBatchName(y) + '</b>\n\n'
                    yf = 1

                i = i + 1
                message += str(i) + '. ' + m['first_name'] + ' '
                # check if valide last_name exists
                if type(m['last_name']) is str:
                    message += m['last_name']

                # Get previous history of member
                memberHistory = Log.objects.filter(member=m['user'], thread=thread).order_by('-timestamp')

                if memberHistory:
                    # find the last time the member send a status update
                    last = memberHistory[0]
                    diff = date.today() - last.timestamp.date()
                    if diff.days > 28:
                        message += ' [ 1M+, '
                    elif diff.days > 21:
                        message += ' [ 3W+, '
                    elif diff.days > 14:
                        message += ' [ 2W+, '
                    elif diff.days > 7:
                        message += ' [ 1W+, '
                    else:
                        message += ' [ ' + str(diff.days) + 'D, '

                    # find count of status updates send by member in last month
                    month_ago = d - timedelta(days=31)
                    count = memberHistory.filter(timestamp__gt=month_ago).count()
                    message += str(count) + '/31 ]'

                # if member has no previous history
                else:
                    message += ' [ NSB ]'

                message += '\n'

    if thread.footerMessage:
        message += '\n<i>'+ thread.footerMessage +'</i>'

    # Log message
    print(message)

    group = Group.objects.get(thread=thread)

    # Send Message through Telegram Bot
    bot = telegram.Bot(token=group.telegramBot)
    bot.send_message(
        chat_id=group.telegramGroup,
        text=message,
        parse_mode=telegram.ParseMode.HTML
    )