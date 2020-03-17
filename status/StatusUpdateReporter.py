from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from pytz import timezone
import telegram
from status.models import Thread, DailyLog, Message, StatusException
from members.models import Group
from members.models import Profile as UserProfile


class ReportMaker(object):

    def __init__(self, d, thread_id):
        self.date = d
        self.thread = Thread.objects.get(id=thread_id)
        self.membersToBeKicked = self.kickMembers()
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
        return UserProfile.objects.filter(user__in=members, batch=year)

    @staticmethod
    def getLastSendStr(last_send):
        message = ''
        diff = last_send + 1
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

    @staticmethod
    def getLastSend(last_send):
        diff = last_send + 1
        return diff

    def getMemberLastRequiredDate(self, member):
        return DailyLog.objects.filter(thread=self.thread, members=member, date__lt=self.date).order_by(
            '-date').first().date

    def getMemberLastSend(self, member):
        obj = DailyLog.objects.filter(thread=self.thread, members=member, date__lt=self.date).exclude(
            didNotSend=member).exclude(invalidUpdates=member).order_by('-date').first()
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
                i = i + 1
                message += str(i) + '. ' + self.getName(member.user)
                profile = UserProfile.objects.get(user=member.user)
                lastSend = profile.didNotSendStreak
                if lastSend:
                    profile.didNotSendStreak = self.getLastSend(int(lastSend))
                    lastSend = self.getLastSendStr(int(lastSend))
                    profile.save()
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
            message += '\n\n<b>&#8987; LATE (' + str(lateCount) + ') : </b> \n\n'
            i = 0
            for member in late_members.all():
                i = i + 1
                timestamp = Message.objects.filter(thread=self.thread, member=member, date=self.date).order_by(
                    '-timestamp').first().timestamp
                message += str(i) + '. ' + self.getName(member) + ' [' + timestamp.astimezone(
                    timezone('Asia/Kolkata')).strftime('%I:%M %p') + '] \n'
        return message

    def getInvalidUpdatesReport(self, invalidUpdates):
        invalidUpdatesCount = invalidUpdates.count()
        message = ''
        if invalidUpdatesCount > 0:
            message += '\n\n<b>⚠️ INVALID STATUS UPDATES (' + str(invalidUpdatesCount) + ') : </b> \n\n'
            i = 0
            for member in invalidUpdates.all():
                i = i + 1
                profile = UserProfile.objects.get(user=member)
                lastSend = profile.didNotSendStreak
                profile.didNotSendStreak = self.getLastSend(int(lastSend))
                message += str(i) + '. ' + self.getName(member) + '\n'
        return message

    def getKickMembersReport(self, kickedOutMembers):
        kickedOutMembersCount = len(kickedOutMembers)
        message = ''
        if kickedOutMembersCount > 0:
            message += '\n\n<b>❌ PEOPLE WHO ARE KICKED (' + str(kickedOutMembersCount) + ') : </b> \n\n'
            i = 0
            for member in kickedOutMembers:
                i = i + 1
                message += str(i) + '. ' + self.getName(member) + '\n'
        return message

    def generateDailyReport(self):
        date = self.date
        thread = self.thread
        try:
            log = DailyLog.objects.get(date=date, thread=thread)
            allowKick = Thread.objects.get(name=thread).allowBotToKick

            totalMembers = log.members.count()
            didNotSendCount = log.didNotSend.count()
            invalidUpdatesCount = log.invalidUpdates.count()
            sendCount = totalMembers - (didNotSendCount + invalidUpdatesCount)

            message = '<b>Daily Status Update Report</b> \n\n &#128197; ' + date.strftime(
                '%d %B %Y') + ' | &#128228; ' + str(sendCount) + '/' + str(totalMembers) + ' Members'

            message += '\n\n<b>' + self.getPercentageSummary(sendCount, totalMembers) + '</b>'
            message += self.getInvalidUpdatesReport(log.invalidUpdates)
            if allowKick:
                message += self.getKickMembersReport(self.membersToBeKicked)
            message += self.getLateReport(log.late)
            message += self.generateDidNotSendReport(log.didNotSend)
            if thread.footerMessage:
                message += '\n<i>' + thread.footerMessage + '</i>'

            return message

        except ObjectDoesNotExist:
            raise

    def kickMembers(self):
        shouldKick = []
        date = self.date
        thread = self.thread
        try:
            telegramAgents = []
            groups = Group.objects.filter(thread_id=thread.id, statusUpdateEnabled=True)
            for group in groups:
                obj = [group.telegramBot, group.telegramGroup]
                if obj not in telegramAgents:
                    telegramAgents.append(obj)

            log = DailyLog.objects.get(date=date, thread=thread)
            members = log.didNotSend.all()
            for agent in telegramAgents:
                bot = telegram.Bot(token=agent[0])
                for member in members:
                    userProfile = UserProfile.objects.get(user=member)
                    lastSend = userProfile.didNotSendStreak
                    if lastSend:
                        try:
                            status = bot.getChatMember(chat_id=agent[1], user_id=userProfile.telegram_id).status
                            if int(lastSend) > thread.noOfDays:
                                kick = True
                                exceptions = StatusException.objects.filter(isPaused=True)
                                for exception in exceptions:
                                    if member == exception.user:
                                        kick = False
                                        break
                                if kick and status != "left":
                                    shouldKick.append(member)
                        except:
                            pass

            return shouldKick

        except ObjectDoesNotExist:
            raise
