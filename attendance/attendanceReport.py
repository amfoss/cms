import telegram
from datetime import date, datetime, timedelta
from members.models import Profile, Group
from attendance.models import Log

from pytz import timezone


def getPercentageSummary(Count, Total):
    if Count / Total >= 1:
        return 'Everyone are in the lab today! &#128079;'
    elif Count / Total > 0.90:
        return 'More than 90% of members are in the lab today.'
    elif Count / Total > 0.75:
        return 'More than 75% of members are in the lab today.'
    elif Count / Total < 0.50:
        return 'Less than 50% of members are in the lab today.'
    elif Count / Total < 0.25:
        return 'Less than 25% of members are in the lab today.'
    elif Count / Total < 0.10:
        return 'Less than 10% of members are in the lab today.'
    return ''


def getName(first, last):
    name = first
    if last:
        name += ' ' + last
    return name


def getBatchName(y):
    now = datetime.now()
    year = int(now.strftime("%Y"))
    if y == year:
        return 'First Year Batch'
    elif y + 1 == year:
        return 'Second Year Batch'
    elif y + 2 == year:
        return 'Third Year Batch'
    elif y + 3 == year:
        return 'Fourth Year Batch'


def generateAttendanceReport(d, log, MembersSentCount, module):
    groupMembers = Group.objects.filter(module=module).values('members')
    groupProfiles = Profile.objects.filter(user__in=groupMembers)
    MemberCount = groupProfiles.count()

    # Get member profile data from CMS
    members_list = groupProfiles.values('user', 'first_name', 'last_name', 'email', 'batch').order_by('batch')

    # Title for the Attendance Report in Telegram
    message = '<b>Attendance Report</b> \n\n &#128197; ' + d.strftime(
        '%d %B %Y') + ' | &#128228; ' + str(MembersSentCount) + '/' + str(MemberCount) + ' Members'

    # Send summary based on percentage of members coming to lab
    message += '\n\n<b>' + getPercentageSummary(MembersSentCount, MemberCount) + '</b>'

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
            if m['user'] not in log.user and y == m['batch']:
                if not mf:
                    message += '''\n\n<b>&#128561; DID NOT CAME TO LAB: </b> \n'''
                    mf = 1
                if not yf:
                    message += '\n<b>' + getBatchName(y) + '</b>\n\n'
                    yf = 1

                i = i + 1
                message += str(i) + '. ' + m['first_name'] + ' '
                # check if last_name exists
                if type(m['last_name']) is str:
                    message += m['last_name']

                # Get previous history of member
                memberHistory = Log.objects.filter(member=m['user'], module=module).order_by('-timestamp')

                if memberHistory:
                    # find the last time member came to lab
                    last = memberHistory[0]
                    diff = date.today() - timedelta(days=1) - last.timestamp.date()
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

    if module.footerMessage:
        message += '\n<i>' + module.footerMessage + '</i>'

    # Log message
    print(message)

    group = Group.objects.get(module=module)

    # Send Message through Telegram Bot
    bot = telegram.Bot(token=group.telegramBot)
    bot.send_message(
        chat_id=group.telegramGroup,
        text=message,
        parse_mode=telegram.ParseMode.HTML
    )