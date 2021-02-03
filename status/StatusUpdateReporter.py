from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from pytz import timezone
import telegram
from status.models import Thread, DailyLog, Message, StatusException
from members.models import Group
from members.models import Profile as UserProfile
from status.discord import Discord


class ReportMaker(object):

    def __init__(self, d, thread_id, isTelegram):
        self.date = d
        self.thread = Thread.objects.get(id=thread_id)
        self.membersToBeKicked = self.kickMembers()
        self.isTelegram = isTelegram
        self.message = self.generateDailyReport()

    @staticmethod
    def getPercentageSummary(send, total, isTelegram):
        if send / total == 1:
            if isTelegram:
                return 'Everyone has sent their Status Updates today! &#128079;'
            else:
                return 'Everyone has sent their Status Updates today!  :clap:'
        elif send / total > 0.90:
            return 'More than 90% of members sent their status update today.'
        elif send / total > 0.75:
            return 'More than 75% of members sent their status update today.'
        elif send / total > 0.50:
            return 'More than 50% of members sent their status update today.'
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
    def getLastSendStr(last_send, expected_date):
        message = ''
        diff = abs(expected_date - last_send)
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

    @staticmethod
    def getLastSend(last_send, expected_date):
        diff = abs(expected_date - last_send)
        diff = diff.days + 1
        return diff

    def getMemberLastRequiredDate(self, member):
        return DailyLog.objects.filter(thread=self.thread, members=member, date__lt=self.date).order_by(
            '-date').first().date

    def getNSBMemberLastRequiredDate(self, member):
        return DailyLog.objects.filter(thread=self.thread, members=member, date__lte=self.date).order_by(
            '-date').last().date

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
            if self.isTelegram:
                message = '\n<b>' + self.getBatchName(year) + ' (' + str(m.count()) + ')' + '</b>\n\n'
            else:
                message = '\n **' + self.getBatchName(year) + ' (' + str(m.count()) + ')' + '** \n\n'
            i = 0
            for member in m:
                i = i + 1
                lastSend = self.getMemberLastSend(member.user)
                message += str(i) + '. ' + self.getName(member.user)
                if lastSend:
                    lastSend = self.getLastSendStr(lastSend.date(),
                                                   self.getMemberLastRequiredDate(member.user))
                    memberHistory = self.getMemberHistory(member.user)
                    message += ' [ ' + lastSend + ', ' + memberHistory + ']'
                else:
                    lastSend = self.getLastSendStr(self.date, self.getNSBMemberLastRequiredDate(member.user))
                    message += ' [ ' + lastSend + ', NSB ]'
                message += '\n'
        return message

    def generateDidNotSendReport(self, members):
        now = datetime.now()
        year = int(now.strftime("%Y"))
        didNotSendCount = members.count()
        message = ''
        if didNotSendCount > 0:
            if self.isTelegram:
                message = '\n\n<b>&#128561; DID NOT SEND (' + str(didNotSendCount) + ') : </b> \n'
            else:
                message = '\n\n **  :scream:  DID NOT SEND (' + str(didNotSendCount) + ') : ** \n'
            message += self.generateBatchWiseDNSReport(members, year - 1)
            message += self.generateBatchWiseDNSReport(members, year - 2)
            message += self.generateBatchWiseDNSReport(members, year - 3)
            message += self.generateBatchWiseDNSReport(members, year - 4)
        return message

    def getLateReport(self, late_members):
        lateCount = late_members.count()
        message = ''
        if lateCount > 0:
            if self.isTelegram:
                message += '\n\n<b>&#8987; LATE (' + str(lateCount) + ') : </b> \n\n'
            else:
                message += '\n\n **  :hourglass:  LATE (' + str(lateCount) + ') : ** \n\n'
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
            if self.isTelegram:
                message += '\n\n<b>⚠️ INVALID (' + str(invalidUpdatesCount) + ') : </b> \n\n'
            else:
                message += '\n\n **  :warning:  INVALID (' + str(invalidUpdatesCount) + ') : ** \n\n'
            i = 0
            for member in invalidUpdates.all():
                i = i + 1
                message += str(i) + '. ' + self.getName(member) + '\n'
        return message

    def getKickMembersReport(self, kickedOutMembers):
        kickedOutMembersCount = len(kickedOutMembers)
        message = ''
        if kickedOutMembersCount > 0:
            if self.isTelegram:
                message += '\n\n<b>❌ KICKED (' + str(kickedOutMembersCount) + ') : </b> \n\n'
            else:
                message += '\n\n **  :x:  KICKED (' + str(kickedOutMembersCount) + ') : ** \n\n'
            i = 0
            for member in kickedOutMembers:
                i = i + 1
                message += str(i) + '. ' + self.getName(member) + '\n'
        return message

    def generateDailyReport(self):
        date = self.date
        thread = self.thread
        updates = Message.objects.filter(date=date, thread=thread).order_by('timestamp')
        first = UserProfile.objects.get(user=updates[0].member)
        last = UserProfile.objects.get(user=list(reversed(updates))[0].member)
        try:
            log = DailyLog.objects.get(date=date, thread=thread)
            allowKick = Thread.objects.get(name=thread).allowBotToKick

            totalMembers = log.members.count()
            didNotSendCount = log.didNotSend.count()
            invalidUpdatesCount = log.invalidUpdates.count()
            sendCount = totalMembers - (didNotSendCount + invalidUpdatesCount)
            if self.isTelegram:
                message = '<b>Daily Status Update Report</b> \n\n &#128197; ' + date.strftime(
                '%d %B %Y') + ' | &#128228; ' + str(sendCount) + '/' + str(totalMembers) + ' Members'

                message += '\n\n<b>' + self.getPercentageSummary(sendCount, totalMembers, self.isTelegram) + '</b>'
            else:
                message = '**Daily Status Update Report** \n\n  :calendar:  ' + date.strftime(
                    '%d %B %Y') + ' |  :outbox_tray:  ' + str(sendCount) + '/' + str(totalMembers) + ' Members'

                message += '\n\n **' + self.getPercentageSummary(sendCount, totalMembers, self.isTelegram) + '**'
            message += self.getInvalidUpdatesReport(log.invalidUpdates)
            if allowKick:
                message += self.getKickMembersReport(self.membersToBeKicked)
            if updates.count() > 0:
                if self.isTelegram:
                    message += '\n\n<b>&#11088; First : </b>' + first.first_name + ' ' + first.last_name + \
                           ' (' + updates[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime(
                    '%I:%M %p') + ')' + '\n'
                    message += '<b>&#128012; Last : </b>' + last.first_name + ' ' + last.last_name + \
                           ' (' + list(reversed(updates))[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime(
                    '%I:%M %p') + ')' + '\n'
                else:
                    message += '\n\n**  :star:  First : **' + first.first_name + ' ' + first.last_name + \
                            ' (' + updates[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime(
                        '%I:%M %p') + ')' + '\n'
                    message += '**  :snail:  Last : **' + last.first_name + ' ' + last.last_name + \
                            ' (' + list(reversed(updates))[0].timestamp.astimezone(timezone('Asia/Kolkata')).strftime(
                        '%I:%M %p') + ')' + '\n'
            message += self.generateDidNotSendReport(log.didNotSend)
            if thread.footerMessage:
                if self.isTelegram:
                    message += '\n<i>' + thread.footerMessage + '</i>'
                else:
                    message += '\n_' + thread.footerMessage + '_'

            return message

        except ObjectDoesNotExist:
            raise

    def kickMembers(self):
        shouldKick = []
        date = self.date
        thread = self.thread
        try:
            telegramAgents = []
            discordAgents = []
            groups = Group.objects.filter(thread_id=thread.id, statusUpdateEnabled=True)
            for group in groups:
                obj = [group.telegramBot, group.telegramGroup]
                discord_obj = [group.discordBot, group.discordGroup, group.discordChannel]
                if obj not in telegramAgents:
                    telegramAgents.append(obj)
                if discord_obj not in discordAgents:
                    discordAgents.append(discord_obj)

            log = DailyLog.objects.get(date=date, thread=thread)
            members = log.didNotSend.all()

            for agent in telegramAgents:
                bot = telegram.Bot(token=agent[0])
                for member in members:
                    member = self.checkKickException(member, bot=bot)
                    if member:
                        shouldKick.append(member)

            for discordAgent in discordAgents:
                for member in members:
                    member = self.checkKickException(member)
                    if member and member not in shouldKick:
                        shouldKick.append(member)
                

        except ObjectDoesNotExist:
            raise

        return shouldKick
    
    def checkKickException(self, member, bot = None):
        date = self.date
        thread = self.thread
        userProfile = UserProfile.objects.get(user=member)
        lastSend = self.getMemberLastSend(member)

        if lastSend:
            lastSend = self.getLastSend(lastSend.date(),
                                        self.getMemberLastRequiredDate(member))
        else:
            lastSend = self.getLastSend(self.date, self.getNSBMemberLastRequiredDate(member))
        try:
            if bot:
                status = bot.getChatMember(chat_id=agent[1], user_id=userProfile.telegram_id).status
            else:
                status = "present"
            if lastSend > thread.noOfDays:
                kick = True
                exceptions = StatusException.objects.filter(isPaused=True)
                if exceptions:
                    for exception in exceptions:
                        if member == exception.user:
                            if exception.start_date <= date.today() <= exception.end_date:
                                kick = False
                                break
                            else:
                                exception.isPaused = False
                if kick and status != "left":
                    return member
        except:
            pass
        
        return None
