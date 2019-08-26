import telegram
from status.management.fetch_status_updates import DailyStatus
from datetime import date, datetime, timedelta
from members.models import Profile
from status.models import StatusRegister
from framework import settings
from pytz import timezone
from operator import itemgetter

from pytz import timezone

def sendReport(maxt, mint, thread, groupID):

    # Get member profile data from CMS
    members_list = Profile.objects.values('user', 'first_name', 'last_name', 'email', 'batch').order_by('batch')

    # Get total count of members
    MemberCount = Profile.objects.filter(batch__gt=d.year - 4).count()

    # Get All Status Update Entries for the Day
    updates = StatusRegister.objects.filter(timestamp__gt=mint, timestamp__lt=maxt, thread=thread).order_by('timestamp')

    # Title for the Status Update Report for Telegram
    message = '<b>Daily Status Update Report</b> \n\n &#128197; ' + d.strftime(
        '%d %B %Y') + ' | &#128228; ' + str(MembersSentCount) + '/' + str(MemberCount) + ' Members'

    # Send summary based on percentage of members sending status updates
    if MembersSentCount / MemberCount > 0.90:
        message += '''\n\n<b>More than 90% of members sent their status update today.</b>'''

    elif MembersSentCount / MemberCount > 0.75:
        message += '''\n\n<b>More than 75% of members sent their status update today.</b>'''

    elif MembersSentCount / MemberCount < 0.25:
        message += '''\n\n<b>Less than 25% of members sent their status update today.</b>'''

    elif MembersSentCount / MemberCount < 0.10:
        message += '''\n\n<b>Less than 10% of members sent their status update today.</b>'''

    if MembersSentCount > 0:
        # Find the first person and his/her time to send status update
        first = Profile.objects.get(user=updates[0].member)
        fn = first.first_name
        ft = updates[0].timestamp

        # Find the last person and his/her to send status update
        u = list(reversed(updates))
        last = Profile.objects.get(user=u[0].member)
        ln = last.first_name
        lt = u[0].timestamp

        ## Add Names of First and Last Person to status updates to the message
        message += '''\n\n<b>&#11088; First : </b>'''
        message += fn + ' (' + ft.astimezone(timezone('Asia/Kolkata')).strftime('%I:%M %p') + ')\n'
        message += '''<b>&#128012; Last : </b>'''
        message += ln + ' (' + lt.astimezone(timezone('Asia/Kolkata')).strftime('%I:%M %p') + ')\n'

    # Generate Report for members who have send status update lately
    # Find current time
    now = datetime.now()
    # Find status updates send between due time and now
    lateLogs = StatusRegister.objects.filter(timestamp__gt=maxt, timestamp__lt=now).order_by('timestamp')

    i = 0
    if lateLogs.count() > 0:
        message += '''\n\n<b>&#8987; LATE: </b> \n'''
    for m in members_list:
        obj = lateLogs.filter(member=m['user'])
        if obj:
            i = i + 1
            message += str(i) + '. ' + m['first_name'] + ' [' + str(
                obj[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime('%I:%M %p')) + '] \n'

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
                    message += '\n<b>' + str(y + 4) + ' Batch </b>\n\n'
                    yf = 1

                i = i + 1
                message += str(i) + '. ' + m['first_name'] + ' '
                # check if valide last_name exists
                if type(m['last_name']) is str:
                    message += m['last_name']

                # Get previous history of member
                memberHistory = StatusRegister.objects.filter(member=m['user']).order_by('-timestamp')

                if memberHistory:
                    # find the last time the member send a status update
                    last = memberHistory[0]
                    diff = d - last.timestamp.date()
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
                    message += '[ NSB ]'

                message += '\n'

    if not mf:
        message += '\n\n<b>Everyone has send their Status Updates today! &#128079;</b>\n'

    message += '\n<i>This is an automatically generated message. Please send your status updates daily.</i>'

    # Log message
    print(message)

    # Send Message through Telegram Bot
    bot = telegram.Bot(
        token=settings.TELEGRAM_BOT_TOKEN)
    bot.send_message(
        chat_id=groupID,
        text=message,
        parse_mode=telegram.ParseMode.HTML
    )