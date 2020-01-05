from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from pytz import timezone

from status.models import Thread, DailyLog, Message
from college.models import Profile


class ReportMaker(object):

    def __init__(self, d, thread_id):
        self.date = d
        self.thread = Thread.objects.get(id=thread_id)
        self.message = self.generateDailyReport()

    @staticmethod
    def getPercentageSummary(send, total):
        if send / total == 1:
            return 'Everyone has sent their Status Updates today! &#128079;'
        elif send / total > 0.90:
            return 'More than 90% of members sent their status update today.'
        elif send / total > 0.75:
            return 'More than 75% of members sent their status update today.'
        elif send / total < 0.50:
            return 'Less than 50% of members sent their status update today.'
        elif send / total < 0.25:
            return 'Less than 25% of members sent their status update today.'
        elif send / total < 0.10:
            return 'Less than 10% of members sent their status update today.'
        return ''

    @staticmethod
    def getName(user):
        name = ''
        if user.first_name:
            name = user.first_name
        if user.last_name:
            name += ' ' + user.last_name
        if name == '':
            name = user.username
        return name

    @staticmethod
    def getBatchName(y):
        now = datetime.now()
        year = int(now.strftime("%Y"))
        if y + 1 == year:
            return 'First Year Batch'
        elif y + 2 == year:
            return 'Second Year Batch'
        elif y + 3 == year:
            return 'Third Year Batch'
        elif y + 4 == year:
            return 'Fourth Year Batch'

    @staticmethod
    def groupMembersByBatch(members, year):
        return Profile.objects.filter(user__in=members, admissionYear=year)

    @staticmethod
    def getLastSendStr(last_send, expected_date):
        message = ''
        diff = expected_date - last_send.date()
        diff = diff.days + 1
        if diff > 28:
            message += '1M+'
        elif diff > 21:
            message += '3W+'
        elif diff > 14:
            message += '2W+'
        elif diff > 7:
            message += '1W+'
        else:
            message += str(diff) + 'D'
        return message

    def getMemberLastRequiredDate(self, member):
        return DailyLog.objects.filter(thread=self.thread, members=member, date__lt=self.date).order_by('-date').first().date

    def getMemberLastSend(self, member):
        obj = DailyLog.objects.filter(thread=self.thread, members=member, date__lt=self.date).exclude(didNotSend=member).order_by('-date').first()
        if obj:
            return Message.objects.filter(thread=self.thread, member=member, date=obj.date)[0].timestamp
        else:
            return None

    def getMemberHistory(self, member):
        count = 0
        last30 = DailyLog.objects.filter(thread=self.thread, members=member).order_by('-date')[:30]
        for d in last30:
            if member not in d.didNotSend.all():
                count = count + 1
        return str(count) + '/30'

    def generateBatchWiseDNSReport(self, members, year):
        m = self.groupMembersByBatch(members.all(), year)
        message = ''
        if m.count() > 0:
            message = '\n<b>' + self.getBatchName(year) + ' (' + str(m.count()) + ')' + '</b>\n\n'
            i = 0
            for member in m:
                i = i+1
                lastSend = self.getMemberLastSend(member.user)
                message += str(i) + '. ' + self.getName(member.user)
                if lastSend:
                    lastSend = self.getLastSendStr(lastSend,
                                                   self.getMemberLastRequiredDate(member.user))
                    memberHistory = self.getMemberHistory(member.user)
                    message += ' [ ' + lastSend + ', ' + memberHistory + ']'
                else:
                    message += ' [ NSB ]'
                message += '\n'
        return message

    def generateDidNotSendReport(self, members):
        now = datetime.now()
        year = int(now.strftime("%Y"))
        didNotSendCount = members.count()
        message = ''
        if didNotSendCount > 0:
            message = '\n\n<b>&#128561; DID NOT SEND (' + str(didNotSendCount) + ') : </b> \n'
            message += self.generateBatchWiseDNSReport(members, year)
            message += self.generateBatchWiseDNSReport(members, year - 1)
            message += self.generateBatchWiseDNSReport(members, year - 2)
            message += self.generateBatchWiseDNSReport(members, year - 3)
        return message

    def getLateReport(self, late_members):
        lateCount = late_members.count()
        message = ''
        if lateCount > 0:
            message += '\n\n<b>&#8987; LATE (' + str(lateCount) + ') : </b> \n'
            i = 0
            for member in late_members.all():
                i = i + 1
                timestamp = Message.objects.filter(thread=self.thread, member=member, date=self.date).order_by(
                    '-timestamp').first().timestamp
                message += str(i) + '. ' + self.getName(member) + ' [' + timestamp.astimezone(
                    timezone('Asia/Kolkata')).strftime('%I:%M %p') + '] \n'
        return message

    def generateDailyReport(self):
        date = self.date
        thread = self.thread
        try:
            log = DailyLog.objects.get(date=date, thread=thread)

            totalMembers = log.members.count()
            didNotSendCount = log.didNotSend.count()
            sendCount = totalMembers - didNotSendCount

            message = '<b>Daily Status Update Report</b> \n\n &#128197; ' + date.strftime(
                '%d %B %Y') + ' | &#128228; ' + str(sendCount) + '/' + str(totalMembers) + ' Members'

            message += '\n\n<b>' + self.getPercentageSummary(sendCount, totalMembers) + '</b>'
            message += self.getLateReport(log.late)
            message += self.generateDidNotSendReport(log.didNotSend)
            if thread.footerMessage:
                message += '\n<i>' + thread.footerMessage + '</i>'

            return message

        except ObjectDoesNotExist:
            raise
